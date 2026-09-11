#!/usr/bin/env python3
"""
publish_instagram.py — Layer 8 of the open-source stack
=========================================================
Publish a Reel to Instagram via Instagram Graph API (Instagram Login flow).

Pipeline (per docs at developers.facebook.com/docs/instagram-platform):
  1. ig_create_reel_container()  — POST /{ig-user-id}/media with
                                    media_type=REELS, video_url, caption → container_id.
  2. ig_wait_until_finished()    — poll GET /{container_id}?fields=status_code
                                    until FINISHED (or ERROR/EXPIRED).
  3. ig_publish_reel()           — POST /{ig-user-id}/media_publish?creation_id={cid}
                                    → media_id (final published Reel).

Required env vars:
  IG_ACCESS_TOKEN  — IGAA... long-lived token (60 days, refreshable)
  IG_USER_ID       — numeric Instagram user id

Caveats (see research/04_instagram_reels_algorithm.md §3.5):
  - video_url MUST be publicly reachable (IG fetches it).
  - Container expires in 24h if not published.
  - 25 posts/24h limit, 200 API calls/h.
  - Long-lived token refresh: call /refresh_access_token before expiry
    (use ig_refresh_token() weekly).

Usage:
    python3 publish_instagram.py --video-url https://cdn.com/x.mp4 \\
        --caption "Hook #reels #whopclips" \\
        --cover-url https://cdn.com/cover.jpg
    python3 publish_instagram.py info
    python3 publish_instagram.py refresh-token
"""
from __future__ import annotations

import argparse
import json
import os
import sys
import time
from pathlib import Path
from typing import Any, Dict, Optional

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _common import (  # noqa: E402
    log, get_logger, write_json, run, http_session,
    state_set, state_get, env_required, env_optional,
)

log = get_logger("publish_instagram")

GRAPH_API = "https://graph.instagram.com/v21.0"
HTTP_TIMEOUT = 30
POLL_INTERVAL_SEC = 5
POLL_MAX_WAIT_SEC = 600  # 10 min


# ---------------------------------------------------------------------------
# Client
# ---------------------------------------------------------------------------
class InstagramPublisher:
    def __init__(self, access_token: Optional[str] = None,
                 user_id: Optional[str] = None):
        self.access_token = access_token or os.environ.get("IG_ACCESS_TOKEN")
        self.user_id = user_id or os.environ.get("IG_USER_ID")
        if not self.access_token or not self.user_id:
            raise SystemExit("IG_ACCESS_TOKEN and IG_USER_ID must be set")
        self.s = http_session()

    # -- Step 1 --
    def create_reel_container(self, video_url: str, caption: str,
                               cover_url: Optional[str] = None,
                               share_to_fb: Optional[bool] = None,
                               location_id: Optional[str] = None,
                               thumb_offset_ms: Optional[int] = None) -> str:
        """Create a Reel container. Returns container_id."""
        params = {
            "media_type":   "REELS",
            "video_url":    video_url,
            "caption":      caption[:2200],
            "access_token": self.access_token,
        }
        if cover_url:           params["cover_url"] = cover_url
        if share_to_fb is not None:
            params["share_to_fb"] = "true" if share_to_fb else "false"
        if location_id:         params["location_id"] = location_id
        if thumb_offset_ms:     params["thumb_offset"] = str(thumb_offset_ms)

        r = self.s.post(f"{GRAPH_API}/{self.user_id}/media",
                        data=params, timeout=HTTP_TIMEOUT)
        r.raise_for_status()
        j = r.json()
        if "id" not in j:
            raise RuntimeError(f"container creation failed: {j}")
        return j["id"]

    # -- Step 2 --
    def get_container_status(self, container_id: str) -> str:
        """Returns 'IN_PROGRESS', 'FINISHED', 'ERROR', or 'EXPIRED'."""
        r = self.s.get(f"{GRAPH_API}/{container_id}",
                        params={"fields": "status_code",
                                "access_token": self.access_token},
                        timeout=HTTP_TIMEOUT)
        r.raise_for_status()
        return r.json().get("status_code", "ERROR")

    def wait_until_finished(self, container_id: str,
                            interval_sec: int = POLL_INTERVAL_SEC,
                            max_wait_sec: int = POLL_MAX_WAIT_SEC) -> str:
        """Block until FINISHED or raise."""
        log.info(f"Polling container {container_id} (max {max_wait_sec}s)")
        start = time.time()
        last_status = None
        while time.time() - start < max_wait_sec:
            s = self.get_container_status(container_id)
            if s != last_status:
                log.info(f"   status: {s} ({int(time.time() - start)}s)")
                last_status = s
            if s == "FINISHED":
                return s
            if s in ("ERROR", "EXPIRED"):
                raise RuntimeError(f"container {container_id} status={s}")
            time.sleep(interval_sec)
        raise TimeoutError(f"container not FINISHED in {max_wait_sec}s")

    # -- Step 3 --
    def publish_reel(self, container_id: str) -> str:
        """Publish the finished container. Returns media_id."""
        r = self.s.post(f"{GRAPH_API}/{self.user_id}/media_publish",
                        data={"creation_id": container_id,
                              "access_token": self.access_token},
                        timeout=HTTP_TIMEOUT)
        r.raise_for_status()
        j = r.json()
        if "id" not in j:
            raise RuntimeError(f"publish failed: {j}")
        return j["id"]

    # -- End-to-end --
    def publish_reel_full(self, video_url: str, caption: str,
                          cover_url: Optional[str] = None) -> Dict[str, Any]:
        """Full flow: container → wait → publish. Returns media_id + permalink."""
        log.info(f"[1/3] Creating Reel container (video_url={video_url[:60]}…)")
        cid = self.create_reel_container(video_url, caption, cover_url=cover_url)
        log.info(f"   container_id: {cid}")

        log.info("[2/3] Waiting for FINISHED…")
        self.wait_until_finished(cid)

        log.info("[3/3] Publishing…")
        media_id = self.publish_reel(cid)
        permalink = f"https://instagram.com/reel/{media_id}"
        log.info(f"   media_id: {media_id}")
        return {
            "container_id": cid,
            "media_id": media_id,
            "permalink": permalink,
        }

    # -- Insights --
    def insights(self, media_id: str) -> Dict[str, Any]:
        """Fetch Reels Insights."""
        r = self.s.get(f"{GRAPH_API}/{media_id}/insights",
                       params={
                           "metric": "views,likes,comments,saves,shares,follows,"
                                     "profile_visits,reach,total_views,video_views,"
                                     "clips_replays_count",
                           "access_token": self.access_token,
                       },
                       timeout=HTTP_TIMEOUT)
        r.raise_for_status()
        return r.json()

    # -- Token management --
    def refresh_token(self) -> str:
        """Refresh long-lived token. Call weekly."""
        r = self.s.get(f"{GRAPH_API}/refresh_access_token",
                       params={"grant_type": "ig_refresh_token",
                               "access_token": self.access_token},
                       timeout=HTTP_TIMEOUT)
        r.raise_for_status()
        new = r.json()["access_token"]
        log.info(f"Token refreshed (new len={len(new)})")
        return new

    def get_me(self) -> Dict[str, Any]:
        """Sanity check: returns {id, username, followers_count, media_count}."""
        r = self.s.get(f"{GRAPH_API}/me",
                       params={"fields": "id,username,followers_count,media_count",
                               "access_token": self.access_token},
                       timeout=HTTP_TIMEOUT)
        r.raise_for_status()
        return r.json()


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------
def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)

    p_pub = sub.add_parser("publish", help="Publish a Reel")
    p_pub.add_argument("--video-url", required=True,
                       help="Publicly reachable MP4 URL")
    p_pub.add_argument("--caption", required=True,
                       help="Caption with hashtags (max 2200 chars)")
    p_pub.add_argument("--cover-url", default=None)

    p_insights = sub.add_parser("insights", help="Fetch Reel insights")
    p_insights.add_argument("--media-id", required=True)

    sub.add_parser("info", help="Print IG profile sanity check")
    sub.add_parser("refresh-token", help="Refresh long-lived token (call weekly)")

    args = ap.parse_args()
    pub = InstagramPublisher()

    if args.cmd == "info":
        print(json.dumps(pub.get_me(), indent=2))
        return

    if args.cmd == "refresh-token":
        new = pub.refresh_token()
        print(f"NEW_ACCESS_TOKEN={new}")
        return

    if args.cmd == "insights":
        ins = pub.insights(args.media_id)
        print(json.dumps(ins, indent=2))
        return

    if args.cmd == "publish":
        result = pub.publish_reel_full(args.video_url, args.caption,
                                       cover_url=args.cover_url)
        state_set(f"ig_publish:{args.video_url}", result)
        print(json.dumps(result, indent=2))
        return


if __name__ == "__main__":
    main()
