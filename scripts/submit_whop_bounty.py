#!/usr/bin/env python3
"""
submit_whop_bounty.py — Layer 10 of the open-source stack
=========================================================
Submit published clips to Whop Bounty API for Content Rewards payout.

API docs: https://docs.whop.com/api-reference/beta/bounties/
Base URL: https://api.whop.com/api/v1

Pipeline:
  1. list_bounties()             — GET /bounties?status=open&business_goal_type=clipping
                                    Returns all open clipping bounties.
  2. get_bounty(bounty_id)       — GET /bounties/{id}
                                    Detailed bounty info (rules, assets, payout rate).
  3. submit_bounty(bounty_id, urls, caption, file_ids=[])
                                   — POST /bounty_submissions
                                    Submits the deliverable for payout consideration.
  4. list_submissions()          — GET /bounty_submissions?bounty_id=...
                                    Polls status (no webhooks for bounties).
  5. upload_file()               — POST /files (multipart)
                                    Pre-uploads attachments for the deliverable.

Auth:
  - User OAuth token required for submissions (account API key insufficient).
  - Set WHOP_USER_TOKEN env var (Bearer token from "Sign in with Whop" OAuth flow).
  - Optionally WHOP_ACCOUNT_KEY for account-level reads (bounty listing).

Caveats (see research/01_whop_deep_dive.md §4.3):
  - All bounty_submissions require user credential.
  - Bounties do NOT emit webhooks — poll /bounty_submissions once a minute.
  - Public bounty retrieve: GET /bounties/{id} works without auth (only if public).
  - Min escrow floor $5. Whop Clips YouTube clips pay $1.25/1K views.

Usage:
    python3 submit_whop_bounty.py list --business-goal clipping
    python3 submit_whop_bounty.py get --bounty-id bnty_XXX
    python3 submit_whop_bounty.py submit \\
        --bounty-id bnty_XXX \\
        --urls https://www.youtube.com/shorts/ABCDEF \\
        --caption "Vertical cut, 42s. Hook: 'Why most people are broke'"
    python3 submit_whop_bounty.py poll --bounty-id bnty_XXX --max-min 5
"""
from __future__ import annotations

import argparse
import json
import os
import sys
import time
from pathlib import Path
from typing import Any, Dict, List, Optional

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _common import (  # noqa: E402
    log, get_logger, write_json, run, http_session,
    state_set, state_get, DATA_DIR,
)

log = get_logger("submit_whop")

WHOP_API = "https://api.whop.com/api/v1"
WHOP_API_VERSION_DATE = os.environ.get("WHOP_API_VERSION_DATE", "2026-09-11")
HTTP_TIMEOUT = 30
POLL_INTERVAL_SEC = 60  # bounties have no webhooks — poll once per minute


# ---------------------------------------------------------------------------
# Client
# ---------------------------------------------------------------------------
class WhopClient:
    def __init__(self, user_token: Optional[str] = None,
                 account_key: Optional[str] = None):
        self.user_token = user_token or os.environ.get("WHOP_USER_TOKEN")
        self.account_key = account_key or os.environ.get("WHOP_ACCOUNT_KEY")
        if not self.user_token and not self.account_key:
            raise SystemExit("WHOP_USER_TOKEN (for submissions) or "
                             "WHOP_ACCOUNT_KEY (for listing) required")
        # Build the session — use user_token if present (higher privileges)
        token = self.user_token or self.account_key
        self.s = http_session(
            token=token,
            extra_headers={
                "Api-Version-Date": WHOP_API_VERSION_DATE,
                "Content-Type": "application/json",
            },
        )

    # -- 1. List bounties --
    def list_bounties(self, status: str = "open",
                     business_goal_type: Optional[str] = "clipping",
                     country: Optional[str] = None,
                     experience_id: Optional[str] = None,
                     query: Optional[str] = None,
                     order: str = "gross_paid_out_amount",
                     direction: str = "desc",
                     page: int = 1) -> Dict[str, Any]:
        """List bounties. With user_token: all visible. Without: only public."""
        params = {
            "status": status,
            "order": order,
            "direction": direction,
            "page": str(page),
        }
        if business_goal_type:
            params["business_goal_type"] = business_goal_type
        if country:
            params["country"] = country
        if experience_id:
            params["experience_id"] = experience_id
        if query:
            params["query"] = query

        r = self.s.get(f"{WHOP_API}/bounties",
                       params=params, timeout=HTTP_TIMEOUT)
        r.raise_for_status()
        return r.json()

    # -- 2. Get one bounty --
    def get_bounty(self, bounty_id: str) -> Dict[str, Any]:
        """GET /bounties/{id}. Works without auth for public bounties."""
        r = self.s.get(f"{WHOP_API}/bounties/{bounty_id}",
                       timeout=HTTP_TIMEOUT)
        r.raise_for_status()
        return r.json()

    # -- 3. Submit a deliverable --
    def submit_bounty(self, bounty_id: str,
                     urls: List[str],
                     caption: str = "",
                     file_ids: Optional[List[str]] = None,
                     platform: str = "youtube") -> Dict[str, Any]:
        """POST /bounty_submissions with the deliverable.

        Required scope: user credential (account API key insufficient).
        """
        if not self.user_token:
            raise SystemExit("WHOP_USER_TOKEN required for submissions "
                             "(account API key is insufficient)")

        deliverable: Dict[str, Any] = {
            "urls": urls,
            "caption": caption,
            "platform": platform,
        }
        if file_ids:
            deliverable["file_ids"] = file_ids

        body = {
            "bounty_id": bounty_id,
            "deliverable": deliverable,
        }
        log.info(f"POST /bounty_submissions bounty={bounty_id} "
                 f"urls={urls} platform={platform}")
        r = self.s.post(f"{WHOP_API}/bounty_submissions",
                        json=body, timeout=HTTP_TIMEOUT)
        if r.status_code not in (200, 201):
            raise RuntimeError(f"submit failed HTTP {r.status_code}: {r.text}")
        return r.json()

    # -- 4. List submissions (for polling) --
    def list_submissions(self, bounty_id: Optional[str] = None,
                         status: Optional[str] = None) -> Dict[str, Any]:
        """GET /bounty_submissions. Filter by bounty_id and/or status."""
        params = {}
        if bounty_id:
            params["bounty_id"] = bounty_id
        if status:
            params["status"] = status
        r = self.s.get(f"{WHOP_API}/bounty_submissions",
                       params=params, timeout=HTTP_TIMEOUT)
        r.raise_for_status()
        return r.json()

    # -- 5. Public submissions --
    def list_public_submissions(self, bounty_id: str) -> Dict[str, Any]:
        """GET /bounties/{id}/submissions/public. No auth required."""
        r = self.s.get(f"{WHOP_API}/bounties/{bounty_id}/submissions/public",
                       timeout=HTTP_TIMEOUT)
        r.raise_for_status()
        return r.json()

    # -- 6. Upload file (pre-step before submit if attachments needed) --
    def upload_file(self, file_path: str,
                    purpose: str = "bounty_submission") -> Dict[str, Any]:
        """POST /files (multipart/form-data). Returns {id: 'file_XXX'}."""
        if not self.user_token:
            raise SystemExit("WHOP_USER_TOKEN required for file upload")
        if not Path(file_path).exists():
            raise SystemExit(f"File not found: {file_path}")

        # Switch to multipart upload
        headers = {"Authorization": f"Bearer {self.user_token}",
                   "Api-Version-Date": WHOP_API_VERSION_DATE}
        with open(file_path, "rb") as f:
            files = {"file": (Path(file_path).name, f)}
            data = {"purpose": purpose}
            r = http_session().post(
                f"{WHOP_API}/files",
                files=files, data=data,
                headers=headers,
                timeout=HTTP_TIMEOUT * 5,
            )
        if r.status_code not in (200, 201):
            raise RuntimeError(f"file upload failed {r.status_code}: {r.text}")
        return r.json()

    # -- Polling helper --
    def poll_submission_status(self, bounty_id: str,
                                max_min: int = 5,
                                interval_sec: int = POLL_INTERVAL_SEC) -> Dict[str, Any]:
        """Poll GET /bounty_submissions?bounty_id={bounty_id} once per minute
        for max_min. Returns the latest submission(s)."""
        log.info(f"Polling bounty {bounty_id} status every {interval_sec}s "
                 f"for {max_min} min")
        start = time.time()
        last_count = -1
        while time.time() - start < max_min * 60:
            j = self.list_submissions(bounty_id=bounty_id)
            subs = j.get("data", [])
            if len(subs) != last_count:
                log.info(f"   {len(subs)} submissions ({int(time.time() - start)}s)")
                last_count = len(subs)
            # If any submission is approved/denied, return immediately
            for s in subs:
                status = s.get("status")
                if status in ("approved", "denied"):
                    log.info(f"   ⚠ submission {s.get('id')} status={status}")
                    return {"bounty_id": bounty_id, "submissions": subs,
                            "terminal": True}
            time.sleep(interval_sec)
        return {"bounty_id": bounty_id, "submissions": subs or [],
                "terminal": False}


# ---------------------------------------------------------------------------
# Module-level helper used by publish_youtube.py + publish_tiktok.py + publish_instagram.py
# ---------------------------------------------------------------------------
def submit_bounty(bounty_id: str,
                  urls: List[str],
                  caption: str,
                  platform: str = "youtube",
                  video_id: Optional[str] = None) -> Dict[str, Any]:
    """Module-level shortcut. Used by publish_youtube.py auto-submit."""
    client = WhopClient()
    result = client.submit_bounty(
        bounty_id=bounty_id, urls=urls, caption=caption,
        platform=platform,
    )
    state_set(f"whop_submit:{bounty_id}:{video_id or urls[0]}", result)
    return result


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------
def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)

    p_list = sub.add_parser("list", help="List open bounties")
    p_list.add_argument("--business-goal", default="clipping")
    p_list.add_argument("--status", default="open",
                        choices=["scheduled", "open", "closed", "completed",
                                 "canceled"])
    p_list.add_argument("--country", default=None,
                        help="ISO 3166-1 alpha-2 (e.g. US, EG)")
    p_list.add_argument("--order", default="gross_paid_out_amount",
                        choices=["created_at", "gross_paid_out_amount",
                                 "gross_reward_amount"])
    p_list.add_argument("--direction", default="desc",
                        choices=["asc", "desc"])

    p_get = sub.add_parser("get", help="Get a single bounty")
    p_get.add_argument("--bounty-id", required=True)

    p_pub = sub.add_parser("public", help="List public submissions for a bounty")
    p_pub.add_argument("--bounty-id", required=True)

    p_submit = sub.add_parser("submit", help="Submit a deliverable")
    p_submit.add_argument("--bounty-id", required=True)
    p_submit.add_argument("--urls", required=True,
                          help="Comma-separated URLs (TikTok/IG/YT posts)")
    p_submit.add_argument("--caption", default="")
    p_submit.add_argument("--platform", default="youtube",
                          choices=["youtube", "tiktok", "instagram",
                                   "twitter", "facebook"])
    p_submit.add_argument("--file", action="append",
                          help="Local file to upload (can repeat)")

    p_poll = sub.add_parser("poll", help="Poll submissions status")
    p_poll.add_argument("--bounty-id", required=True)
    p_poll.add_argument("--max-min", type=int, default=5)
    p_poll.add_argument("--interval-sec", type=int, default=POLL_INTERVAL_SEC)

    p_sub_list = sub.add_parser("submissions", help="List own submissions")
    p_sub_list.add_argument("--bounty-id", default=None)
    p_sub_list.add_argument("--status", default=None,
                           choices=["in_progress", "submitted", "approved",
                                    "denied"])

    args = ap.parse_args()
    client = WhopClient()

    if args.cmd == "list":
        out = client.list_bounties(
            status=args.status,
            business_goal_type=args.business_goal,
            country=args.country,
            order=args.order,
            direction=args.direction,
        )
        # Pretty print summary
        data = out.get("data", [])
        print(f"\nFound {len(data)} {args.business_goal} bounties "
              f"(status={args.status}, order={args.order} {args.direction})\n")
        for b in data[:30]:
            pay = b.get("gross_reward_amount", "?")
            paid = b.get("gross_paid_out_amount", 0)
            title = (b.get("title") or "")[:60]
            countries = b.get("allowed_country_codes") or []
            print(f"  {b.get('id'):<20} ${pay}/{b.get('reward_currency', 'USD'):>3} "
                  f"(paid ${paid}/{b.get('reward_currency', 'USD')}) "
                  f"countries={','.join(countries[:3]) or 'any':<8} "
                  f"title={title}")
        if len(data) > 30:
            print(f"\n  … {len(data) - 30} more (show first 30)")
        print(f"\nFull JSON: see logs/")
        state_set(f"whop_list:{args.business_goal}:{args.status}", out)
        return

    if args.cmd == "get":
        b = client.get_bounty(args.bounty_id)
        print(json.dumps(b, indent=2))
        return

    if args.cmd == "public":
        ps = client.list_public_submissions(args.bounty_id)
        print(json.dumps(ps, indent=2))
        return

    if args.cmd == "submit":
        urls = [u.strip() for u in args.urls.split(",") if u.strip()]
        file_ids = []
        if args.file:
            for fp in args.file:
                if not Path(fp).exists():
                    log.warning(f"  skip missing file: {fp}")
                    continue
                log.info(f"Uploading attachment: {fp}")
                up = client.upload_file(fp)
                fid = up.get("id")
                if fid:
                    file_ids.append(fid)
        result = client.submit_bounty(
            bounty_id=args.bounty_id,
            urls=urls,
            caption=args.caption,
            file_ids=file_ids or None,
            platform=args.platform,
        )
        state_set(f"whop_submit:{args.bounty_id}:{urls[0]}", result)
        print(json.dumps(result, indent=2))
        return

    if args.cmd == "poll":
        out = client.poll_submission_status(
            bounty_id=args.bounty_id,
            max_min=args.max_min,
            interval_sec=args.interval_sec,
        )
        print(json.dumps(out, indent=2, default=str))
        return

    if args.cmd == "submissions":
        out = client.list_submissions(bounty_id=args.bounty_id,
                                       status=args.status)
        print(json.dumps(out, indent=2, default=str))
        return


if __name__ == "__main__":
    main()
