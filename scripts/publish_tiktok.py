#!/usr/bin/env python3
"""
publish_tiktok.py — Layer 8 of the open-source stack
=====================================================
Publish a vertical short video to TikTok via Content Posting API v2.

Pipeline (per TikTok docs at developers.tiktok.com):
  1. query_creator_info()  — confirm scopes + max duration.
  2. init_video_upload_file()/init_video_upload_url()  — start upload.
  3. upload_video_file()  (if FILE_UPLOAD)  — PUT chunked bytes.
  4. fetch_post_status()  — poll until SUCCESS or FAIL.

Required env vars:
  TIKTOK_CLIENT_KEY, TIKTOK_CLIENT_SECRET, TIKTOK_ACCESS_TOKEN

Scopes required (set in App console):
  video.publish (Direct Post) — needs audit approval for public posts.
  video.upload  (Draft only — no audit needed, but followers won't see it).

Caveats (see research/03_tiktok_algorithm.md §4.6):
  - All unaudited apps post in "private viewing mode" only.
  - Verified domain required for PULL_FROM_URL.
  - Max video duration 300s (5 min). Aim 60-90s sweet spot.
  - Rate limit: 600 req/min per endpoint.
  - No webhooks for content posting — must poll /status/fetch/ every 60s.

Usage:
    python3 publish_tiktok.py --file final.mp4 --caption "Hook here #fyp #whopclips"
    python3 publish_tiktok.py --file final.mp4 --caption "..." --privacy SELF_ONLY
    python3 publish_tiktok.py --video-url https://my-cdn.com/final.mp4 --caption "..."
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
    log, get_logger, write_json, read_json, run, http_session,
    state_set, state_get, env_required, env_optional, DATA_DIR,
)

log = get_logger("publish_tiktok")

TIKTOK_API = "https://open.tiktokapis.com/v2"
HTTP_TIMEOUT = 60
STATUS_POLL_INTERVAL_SEC = 60
STATUS_POLL_MAX_MIN = 10


# ---------------------------------------------------------------------------
# Client
# ---------------------------------------------------------------------------
class TikTokPublisher:
    def __init__(self, access_token: Optional[str] = None,
                 client_key: Optional[str] = None,
                 client_secret: Optional[str] = None):
        self.access_token = access_token or os.environ.get("TIKTOK_ACCESS_TOKEN")
        if not self.access_token:
            raise SystemExit("TIKTOK_ACCESS_TOKEN not set")
        self.client_key = client_key or os.environ.get("TIKTOK_CLIENT_KEY")
        self.client_secret = client_secret or os.environ.get("TIKTOK_CLIENT_SECRET")
        self.s = http_session(token=self.access_token,
                              extra_headers={"Content-Type": "application/json; charset=UTF-8"})

    # -- Step 1 --
    def query_creator_info(self) -> Dict[str, Any]:
        """Returns: creator_username, privacy_level_options, max_video_post_duration_sec."""
        r = self.s.post(f"{TIKTOK_API}/post/publish/creator_info/query/",
                        timeout=HTTP_TIMEOUT)
        r.raise_for_status()
        j = r.json()
        if j.get("error", {}).get("code") != "ok":
            raise RuntimeError(f"creator_info error: {j}")
        return j["data"]

    # -- Step 2a --
    def init_video_upload_file(self, title: str, video_size_bytes: int,
                                chunk_size: int = 10_000_000,
                                total_chunks: int = 5,
                                privacy_level: str = "PUBLIC_TO_EVERYONE",
                                disable_duet: bool = False,
                                disable_comment: bool = False,
                                disable_stitch: bool = False,
                                video_cover_timestamp_ms: int = 1000) -> Dict[str, Any]:
        """Initialize FILE_UPLOAD direct post. Returns publish_id + upload_url."""
        body = {
            "post_info": {
                "title": title[:220],
                "privacy_level": privacy_level,
                "disable_duet": disable_duet,
                "disable_comment": disable_comment,
                "disable_stitch": disable_stitch,
                "video_cover_timestamp_ms": video_cover_timestamp_ms,
            },
            "source_info": {
                "source": "FILE_UPLOAD",
                "video_size": video_size_bytes,
                "chunk_size": chunk_size,
                "total_chunk_count": total_chunks,
            },
        }
        r = self.s.post(f"{TIKTOK_API}/post/publish/video/init/",
                        json=body, timeout=HTTP_TIMEOUT)
        r.raise_for_status()
        j = r.json()
        if j.get("error", {}).get("code") != "ok":
            raise RuntimeError(f"init_video_upload error: {j}")
        return j["data"]

    # -- Step 2b --
    def init_video_upload_url(self, title: str, video_url: str,
                               privacy_level: str = "PUBLIC_TO_EVERYONE",
                               disable_comment: bool = False) -> Dict[str, Any]:
        """Initialize PULL_FROM_URL direct post. Domain must be verified."""
        body = {
            "post_info": {
                "title": title[:220],
                "privacy_level": privacy_level,
                "disable_comment": disable_comment,
                "disable_stitch": False,
                "disable_duet": False,
                "video_cover_timestamp_ms": 1000,
            },
            "source_info": {
                "source": "PULL_FROM_URL",
                "video_url": video_url,
            },
        }
        r = self.s.post(f"{TIKTOK_API}/post/publish/video/init/",
                        json=body, timeout=HTTP_TIMEOUT)
        r.raise_for_status()
        j = r.json()
        if j.get("error", {}).get("code") != "ok":
            raise RuntimeError(f"init_video_upload_url error: {j}")
        return j["data"]

    # -- Step 3 (FILE_UPLOAD only) --
    def upload_video_file(self, upload_url: str, file_path: str,
                          chunk_size: int = 10_000_000) -> int:
        """Upload the video bytes to upload_url via HTTP PUT (chunked)."""
        size = os.path.getsize(file_path)
        total_chunks = (size + chunk_size - 1) // chunk_size

        with open(file_path, "rb") as f:
            for i in range(total_chunks):
                chunk = f.read(chunk_size)
                start = i * chunk_size
                end = start + len(chunk) - 1
                cr = f"bytes {start}-{end}/{size}"
                log.info(f"   chunk {i+1}/{total_chunks} "
                         f"({len(chunk)} bytes, content-range={cr})")
                r = self.s.put(upload_url, data=chunk,
                               headers={
                                   "Content-Range": cr,
                                   "Content-Type": "video/mp4",
                               },
                               timeout=HTTP_TIMEOUT * 2)
                if r.status_code not in (200, 201, 204):
                    raise RuntimeError(f"chunk upload failed {r.status_code}: {r.text}")
        return size

    # -- Step 4 --
    def fetch_post_status(self, publish_id: str) -> Dict[str, Any]:
        """Poll status. Returns {status, fail_code, fail_message}."""
        r = self.s.post(f"{TIKTOK_API}/post/publish/status/fetch/",
                        json={"publish_id": publish_id},
                        timeout=HTTP_TIMEOUT)
        r.raise_for_status()
        j = r.json()
        if j.get("error", {}).get("code") != "ok":
            raise RuntimeError(f"status fetch error: {j}")
        return j["data"]

    def poll_until_done(self, publish_id: str,
                        interval_sec: int = STATUS_POLL_INTERVAL_SEC,
                        max_min: int = STATUS_POLL_MAX_MIN) -> Dict[str, Any]:
        """Block until status == SUCCESS or FAIL. Raises on FAIL."""
        log.info(f"Polling publish_id={publish_id} (max {max_min} min)")
        start = time.time()
        while time.time() - start < max_min * 60:
            st = self.fetch_post_status(publish_id)
            log.info(f"   status: {st.get('status')} "
                     f"({int(time.time() - start)}s elapsed)")
            if st.get("status") == "SUCCESS":
                return st
            if st.get("status") == "FAIL":
                raise RuntimeError(f"upload failed: {st}")
            time.sleep(interval_sec)
        raise TimeoutError(f"post did not complete in {max_min} min")

    # -- End-to-end --
    def publish_from_file(self, file_path: str, title: str,
                          privacy: str = "PUBLIC_TO_EVERYONE",
                          disable_comment: bool = False,
                          chunk_size: int = 10_000_000,
                          poll: bool = True) -> Dict[str, Any]:
        """Full flow: creator_info → init → upload → poll."""
        log.info("[1/4] Querying creator info…")
        ci = self.query_creator_info()
        log.info(f"   creator: {ci.get('creator_username')} "
                 f"max_dur={ci.get('max_video_post_duration_sec')}s "
                 f"privacy_options={ci.get('privacy_level_options')}")

        size = os.path.getsize(file_path)
        total_chunks = (size + chunk_size - 1) // chunk_size

        log.info(f"[2/4] Initializing FILE_UPLOAD (size={size}, "
                 f"chunks={total_chunks}, chunk_size={chunk_size})")
        init = self.init_video_upload_file(
            title=title, video_size_bytes=size,
            chunk_size=chunk_size, total_chunks=total_chunks,
            privacy_level=privacy, disable_comment=disable_comment,
        )
        publish_id = init["publish_id"]
        upload_url = init["upload_url"]
        log.info(f"   publish_id={publish_id}")

        log.info(f"[3/4] Uploading {file_path} to upload_url…")
        self.upload_video_file(upload_url, file_path, chunk_size=chunk_size)

        if not poll:
            return {"publish_id": publish_id, "polled": False, "init": init}

        log.info(f"[4/4] Polling for completion…")
        st = self.poll_until_done(publish_id)
        return {
            "publish_id": publish_id,
            "polled": True,
            "status": st.get("status"),
            "video_id": st.get("video_id"),
            "video_url": st.get("video_url") or
                         f"https://www.tiktok.com/@me/video/{st.get('video_id')}",
            "creator_info": ci,
            "init": init,
        }

    def publish_from_url(self, video_url: str, title: str,
                         privacy: str = "PUBLIC_TO_EVERYONE") -> Dict[str, Any]:
        """PULL_FROM_URL flow: TikTok fetches the video from your CDN.
        Domain must be verified via Developer Portal."""
        log.info("[1/3] Querying creator info…")
        ci = self.query_creator_info()

        log.info(f"[2/3] Initializing PULL_FROM_URL ({video_url})")
        init = self.init_video_upload_url(video_url, title, privacy_level=privacy)
        publish_id = init["publish_id"]
        log.info(f"   publish_id={publish_id}")

        log.info("[3/3] Polling for completion…")
        st = self.poll_until_done(publish_id)
        return {
            "publish_id": publish_id,
            "status": st.get("status"),
            "video_id": st.get("video_id"),
            "creator_info": ci,
        }


# ---------------------------------------------------------------------------
# OAuth flow (helper — used once to get the access_token)
# ---------------------------------------------------------------------------
def oauth_url(client_key: str, redirect_uri: str,
              scopes: str = "video.publish,user.info.basic") -> str:
    """Generate the OAuth authorization URL.
    Paste into a browser → grant → callback contains ?code=... → exchange."""
    return (
        f"https://www.tiktok.com/auth/authorize/?"
        f"client_key={client_key}"
        f"&scope={scopes}"
        f"&response_type=code"
        f"&redirect_uri={redirect_uri}"
        f"&state=random_state_string"
    )


def exchange_code_for_token(client_key: str, client_secret: str,
                             code: str, redirect_uri: str) -> Dict[str, Any]:
    """Exchange the OAuth code for an access_token."""
    s = http_session()
    r = s.post(
        "https://open.tiktokapis.com/v2/oauth/token/",
        data={
            "client_key": client_key,
            "client_secret": client_secret,
            "code": code,
            "grant_type": "authorization_code",
            "redirect_uri": redirect_uri,
        },
        timeout=HTTP_TIMEOUT,
    )
    r.raise_for_status()
    return r.json()


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------
def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)

    p_pub_file = sub.add_parser("file", help="Publish a local file")
    p_pub_file.add_argument("--file", required=True)
    p_pub_file.add_argument("--title", required=True,
                            help="Caption/hashtags (max 220 chars)")
    p_pub_file.add_argument("--privacy", default="PUBLIC_TO_EVERYONE",
                            choices=["PUBLIC_TO_EVERYONE",
                                     "MUTUAL_FOLLOW_FRIENDS", "SELF_ONLY"])
    p_pub_file.add_argument("--no-comment", action="store_true")
    p_pub_file.add_argument("--chunk-size", type=int, default=10_000_000)
    p_pub_file.add_argument("--no-poll", action="store_true")

    p_pub_url = sub.add_parser("url", help="Publish from a public URL")
    p_pub_url.add_argument("--video-url", required=True)
    p_pub_url.add_argument("--title", required=True)
    p_pub_url.add_argument("--privacy", default="PUBLIC_TO_EVERYONE",
                           choices=["PUBLIC_TO_EVERYONE",
                                    "MUTUAL_FOLLOW_FRIENDS", "SELF_ONLY"])

    p_info = sub.add_parser("info", help="Query creator info only")
    p_oauth = sub.add_parser("oauth", help="Print OAuth URL for browser flow")
    p_oauth.add_argument("--redirect-uri", required=True)
    p_oauth.add_argument("--scopes", default="video.publish,user.info.basic")

    args = ap.parse_args()

    if args.cmd == "info":
        pub = TikTokPublisher()
        info = pub.query_creator_info()
        print(json.dumps(info, indent=2))
        return

    if args.cmd == "oauth":
        ck = os.environ.get("TIKTOK_CLIENT_KEY")
        if not ck:
            raise SystemExit("TIKTOK_CLIENT_KEY not set")
        url = oauth_url(ck, args.redirect_uri, args.scopes)
        print("Open this URL in a browser, grant, and capture ?code= from the callback:")
        print(url)
        print("\nThen exchange it:")
        print("  from publish_tiktok import exchange_code_for_token")
        print("  tok = exchange_code_for_token(client_key, client_secret, code, redirect_uri)")
        return

    if args.cmd == "file":
        pub = TikTokPublisher()
        result = pub.publish_from_file(
            file_path=args.file, title=args.title,
            privacy=args.privacy,
            disable_comment=args.no_comment,
            chunk_size=args.chunk_size,
            poll=not args.no_poll,
        )
        state_set(f"tiktok_publish:{args.file}", result)
        print(json.dumps(result, indent=2, default=str))
        return

    if args.cmd == "url":
        pub = TikTokPublisher()
        result = pub.publish_from_url(args.video_url, args.title,
                                      privacy=args.privacy)
        state_set(f"tiktok_publish:{args.video_url}", result)
        print(json.dumps(result, indent=2, default=str))


if __name__ == "__main__":
    main()
