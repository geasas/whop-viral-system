#!/usr/bin/env python3
"""
publish_youtube.py — Layer 8 of the open-source stack
======================================================
Publish a vertical short video to YouTube as a Short via YouTube Data API v3.

Uses Google's official `google-api-python-client` + `google-auth-oauthlib`
for OAuth 2.0 installed-app flow (saved credentials in creds/).

Required files:
  creds/client_secret.json   — OAuth 2.0 Client ID (Desktop app type)
                                downloaded from console.cloud.google.com
  creds/youtube_token.json   — auto-created on first run (refreshable)

Required scope:
  https://www.googleapis.com/auth/youtube.upload   (least privilege)

Caveats (see research/05_youtube_shorts_algorithm.md §3.7):
  - All uploads without API audit are private only.
  - Quota: 10000 units/day, 1 unit per video.insert, 100 uploads/day max.
  - Max file size 256GB.
  - For Shorts: video aspect 9:16, duration <= 3 min.
  - AI content disclosure mandatory since Jul 2025 (use --synthetic flag).

Install:
  pip install google-api-python-client google-auth-oauthlib google-auth-httplib2

Usage:
    python3 publish_youtube.py publish --file final.mp4 \\
        --title "Hook #shorts #whopclips" \\
        --description "Description..." --tags shorts,ytshorts \\
        --synthetic --no-notify
    python3 publish_youtube.py info
"""
from __future__ import annotations

import argparse
import json
import os
import random
import sys
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, Optional

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _common import (  # noqa: E402
    log, get_logger, write_json, run, http_session,
    state_set, state_get, CREDS_DIR,
)

log = get_logger("publish_youtube")

CLIENT_SECRETS_FILE = str(CREDS_DIR / "client_secret.json")
TOKEN_FILE = str(CREDS_DIR / "youtube_token.json")
YOUTUBE_UPLOAD_SCOPE = "https://www.googleapis.com/auth/youtube.upload"
YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"

MAX_RETRIES = 10
RETRIABLE_STATUS_CODES = (500, 502, 503, 504)


# ---------------------------------------------------------------------------
# Auth
# ---------------------------------------------------------------------------
def get_authenticated_service(client_secrets_file: str = CLIENT_SECRETS_FILE,
                               token_file: str = TOKEN_FILE):
    """OAuth 2.0 installed-app flow. Saves token to token_file."""
    try:
        from google.oauth2.credentials import Credentials  # type: ignore
        from google_auth_oauthlib.flow import InstalledAppFlow  # type: ignore
        from google.auth.transport.requests import Request  # type: ignore
        from googleapiclient.discovery import build  # type: ignore
    except ImportError as e:
        raise SystemExit(
            f"Missing google libraries: {e}\n"
            "Run: pip install google-api-python-client "
            "google-auth-oauthlib google-auth-httplib2"
        )

    if not Path(client_secrets_file).exists():
        raise SystemExit(
            f"client_secret.json not found at {client_secrets_file}. "
            "Download from console.cloud.google.com → APIs & Services → "
            "Credentials → OAuth 2.0 Client ID (Desktop app).")

    creds = None
    if Path(token_file).exists():
        creds = Credentials.from_authorized_user_file(token_file,
                                                     [YOUTUBE_UPLOAD_SCOPE])

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                client_secrets_file, [YOUTUBE_UPLOAD_SCOPE])
            creds = flow.run_local_server(port=0)  # opens browser
        Path(token_file).write_text(creds.to_json(), encoding="utf-8")

    return build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION,
                 credentials=creds, cache_discovery=False)


# ---------------------------------------------------------------------------
# Upload
# ---------------------------------------------------------------------------
def upload_short(youtube, file_path: str, title: str,
                 description: str = "", tags: str = "shorts,ytshorts,short",
                 category_id: str = "22",  # People & Blogs
                 privacy: str = "public",
                 publish_at: Optional[str] = None,
                 made_for_kids: bool = False,
                 contains_synthetic_media: bool = False,
                 notify_subscribers: bool = True) -> Dict[str, Any]:
    """Upload a vertical video (9:16, ≤180s) as a YouTube Short."""
    try:
        from googleapiclient.http import MediaFileUpload  # type: ignore
    except ImportError as e:
        raise SystemExit(f"Missing googleapiclient: {e}")

    if not Path(file_path).exists():
        raise SystemExit(f"File not found: {file_path}")

    tags_list = [t.strip() for t in tags.split(",")] if isinstance(tags, str) else tags

    body = {
        "snippet": {
            "title": title[:100],
            "description": description[:5000],
            "tags": tags_list,
            "categoryId": category_id,
            "defaultLanguage": "en",
            "defaultAudioLanguage": "en",
        },
        "status": {
            "privacyStatus": privacy,
            "selfDeclaredMadeForKids": made_for_kids,
            "containsSyntheticMedia": contains_synthetic_media,
            "embeddable": True,
            "license": "youtube",
        },
    }
    if publish_at and privacy == "private":
        body["status"]["publishAt"] = publish_at  # ISO 8601

    log.info(f"Starting resumable upload: {file_path} ({Path(file_path).stat().st_size} bytes)")
    insert_request = youtube.videos().insert(
        part=",".join(body.keys()),
        body=body,
        media_body=MediaFileUpload(file_path, chunksize=-1, resumable=True),
        notifySubscribers=notify_subscribers,
    )
    response = _resumable_upload(insert_request)
    return response


def _resumable_upload(insert_request) -> Dict[str, Any]:
    """Loop until upload completes. Retries on 5xx + network errors."""
    response = None
    error = None
    retry = 0
    while response is None:
        try:
            log.info("   uploading chunk…")
            status, response = insert_request.next_chunk()
            if response is not None:
                if "id" in response:
                    log.info(f"✓ Video ID: {response['id']}")
                else:
                    raise RuntimeError(f"Upload failed: {response}")
        except Exception as e:
            # googleapiclient.errors.HttpError for HTTP errors
            status_code = getattr(getattr(e, "resp", None), "status", None)
            if status_code in RETRIABLE_STATUS_CODES:
                error = f"Retriable HTTP {status_code}: {e}"
            elif "HttpError" in type(e).__name__ and status_code in RETRIABLE_STATUS_CODES:
                error = f"Retriable HTTP {status_code}: {e}"
            else:
                # Retry on transport errors too
                err_str = str(e).lower()
                if any(s in err_str for s in ("connection", "timeout",
                                              "reset", "broken")):
                    error = f"Retriable transport error: {e}"
                else:
                    raise
        if error is not None:
            log.warning(error)
            retry += 1
            if retry > MAX_RETRIES:
                raise RuntimeError(f"Max retries ({MAX_RETRIES}) exceeded")
            sleep_s = min(60, random.uniform(1, 2 ** retry))
            log.info(f"   sleeping {sleep_s:.1f}s, retry {retry}/{MAX_RETRIES}")
            time.sleep(sleep_s)
            error = None
    return response


# ---------------------------------------------------------------------------
# Insights
# ---------------------------------------------------------------------------
def get_video_stats(youtube, video_id: str) -> Dict[str, Any]:
    """Fetch video stats (view count, likes, comments)."""
    r = youtube.videos().list(
        part="statistics,snippet,status",
        id=video_id,
    ).execute()
    items = r.get("items", [])
    if not items:
        return {}
    item = items[0]
    return {
        "video_id": video_id,
        "title": item.get("snippet", {}).get("title"),
        "published_at": item.get("snippet", {}).get("publishedAt"),
        "privacy": item.get("status", {}).get("privacyStatus"),
        "statistics": item.get("statistics", {}),
    }


def get_analytics(youtube, video_ids: list,
                  start_date: str, end_date: str) -> Dict[str, Any]:
    """Fetch YouTube Analytics for given videos + date range.
    Requires the user to have YPP access (or at least channel-level analytics).
    Returns: views, comments, likes, dislikes, shares, subscribersGained, ...
    """
    try:
        r = youtube.reports() if hasattr(youtube, "reports") else None
        if r is None:
            return {"error": "analytics API not available — requires scope "
                             "youtube.readonly in addition to youtube.upload"}
        resp = r.query(
            ids="channel==MINE",
            startDate=start_date,
            endDate=end_date,
            metrics="views,comments,likes,dislikes,shares,"
                    "subscribersGained,subscribersLost,"
                    "estimatedMinutesWatched,averageViewDuration,"
                    "averageViewPercentage,viewersPercentage",
            filters=f"video=={','.join(video_ids)}",
        ).execute()
        return resp
    except Exception as e:
        return {"error": str(e)}


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------
def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)

    p_pub = sub.add_parser("publish", help="Upload a Short")
    p_pub.add_argument("--file", required=True, help="Video file (9:16, ≤180s)")
    p_pub.add_argument("--title", required=True)
    p_pub.add_argument("--description", default="")
    p_pub.add_argument("--tags", default="shorts,ytshorts,short")
    p_pub.add_argument("--category", default="22",
                       help="22=People&Blogs. See https://developers.google.com/youtube/v3/docs/videoCategories/list")
    p_pub.add_argument("--privacy", default="public",
                       choices=["public", "private", "unlisted"])
    p_pub.add_argument("--publish-at", default=None,
                       help="ISO 8601 datetime for scheduled publish "
                            "(requires --privacy=private)")
    p_pub.add_argument("--made-for-kids", action="store_true")
    p_pub.add_argument("--synthetic", action="store_true",
                       help="Declare containsSyntheticMedia (AI content) — "
                            "required since July 2025")
    p_pub.add_argument("--no-notify", action="store_true",
                       help="Don't notify subscribers (recommended for daily Shorts)")
    p_pub.add_argument("--whop-campaign", default=None,
                       help="Whop bounty campaign ID (auto-submit after upload)")

    p_stats = sub.add_parser("stats", help="Get video statistics")
    p_stats.add_argument("--video-id", required=True)

    sub.add_parser("info", help="Auth sanity check")

    args = ap.parse_args()

    if args.cmd == "info":
        yt = get_authenticated_service()
        # sanity: list my own channel
        me = yt.channels().list(part="snippet,statistics", mine=True).execute()
        print(json.dumps(me, indent=2))
        return

    if args.cmd == "stats":
        yt = get_authenticated_service()
        s = get_video_stats(yt, args.video_id)
        print(json.dumps(s, indent=2))
        return

    if args.cmd == "publish":
        yt = get_authenticated_service()
        resp = upload_short(
            yt,
            file_path=args.file,
            title=args.title,
            description=args.description,
            tags=args.tags,
            category_id=args.category,
            privacy=args.privacy,
            publish_at=args.publish_at,
            made_for_kids=args.made_for_kids,
            contains_synthetic_media=args.synthetic,
            notify_subscribers=not args.no_notify,
        )
        video_id = resp.get("id")
        video_url = f"https://www.youtube.com/shorts/{video_id}" if video_id else None
        log.info(f"\n✓ Published: {video_url}")

        state_set(f"yt_publish:{args.file}", {
            "video_id": video_id,
            "url": video_url,
            "title": args.title,
            "privacy": args.privacy,
            "contains_synthetic_media": args.synthetic,
            "submitted_at": datetime.now(timezone.utc).isoformat(),
            "raw_response": resp,
        })

        # Optional Whop bounty integration
        if args.whop_campaign and video_id:
            log.info(f"Auto-submitting to Whop bounty {args.whop_campaign}…")
            try:
                from submit_whop_bounty import submit_bounty  # type: ignore
                sub = submit_bounty(
                    bounty_id=args.whop_campaign,
                    urls=[video_url],
                    caption=args.title,
                    platform="youtube",
                    video_id=video_id,
                )
                state_set(f"yt_whop_submit:{video_id}", sub)
                log.info(f"  ✓ Whop submission: {sub}")
            except Exception as e:
                log.error(f"  ⚠ Whop submit failed: {e}")

        print(json.dumps({
            "video_id": video_id,
            "url": video_url,
            "title": args.title,
            "privacy": args.privacy,
        }, indent=2))


if __name__ == "__main__":
    main()
