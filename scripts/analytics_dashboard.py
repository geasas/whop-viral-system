#!/usr/bin/env python3
"""
analytics_dashboard.py — Layer 9 of the open-source stack
============================================================
Aggregate analytics from TikTok + Instagram + YouTube + Whop bounty payouts.

For each video published by the pipeline, fetches:
  - TikTok: video statistics (views, likes, comments, shares, saves)
             — via TikTok Display API /video/query/ (requires user scopes).
  - Instagram: Reels insights (views, likes, comments, saves, shares, follows)
             — via graph.instagram.com/{media_id}/insights.
  - YouTube: video statistics (viewCount, likeCount, commentCount)
             + YouTube Analytics (estimatedMinutesWatched, averageViewDuration)
             — via googleapis.com/youtube/v3/videos + youtubeAnalytics.v2.
  - Whop:    bounty_submission status + payout amount
             — via api.whop.com/api/v1/bounty_submissions.

Calculates the 5 core metrics (Benchmarks 2026 from research/02_viral_editing_toolkit.md):
  - View Rate       = views / reach    (target >= 85%)
  - AVD             = averageViewDuration / video duration (target >= 70%)
  - Share Rate      = shares / views    (target >= 1.7% — viral threshold)
  - Save Rate       = saves / views     (target >= 2%)
  - Completion Rate = (views - swipeAways) / views (target >= 80% on TT)

Outputs:
  - data/analytics_<YYYY-MM-DD>.csv  — one row per video.
  - data/analytics_<YYYY-MM-DD>.json — full nested JSON.
  - data/analytics_history.csv       — appended every run (long-format).
  - logs/analytics.log               — full log.

State-tracked (state.json): we only refetch videos published more recently
than last_pull_ts (or all if --full).

Usage:
    python3 analytics_dashboard.py pull                  # fetch latest
    python3 analytics_dashboard.py pull --full           # refetch everything
    python3 analytics_dashboard.py summary               # print summary
    python3 analytics_dashboard.py add --video-id ID \\
        --platform tiktok --bounty-id bnty_XXX \\
        --video-file final.mp4 --duration 20.2
"""
from __future__ import annotations

import argparse
import csv
import json
import os
import sys
import time
from datetime import datetime, timezone, timedelta
from pathlib import Path
from typing import Any, Dict, List, Optional

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _common import (  # noqa: E402
    log, get_logger, write_json, read_json, run, http_session,
    state_set, state_get, state_load, state_save, DATA_DIR,
)

log = get_logger("analytics_dashboard")

TIKTOK_API = "https://open.tiktokapis.com/v2"
GRAPH_API = "https://graph.instagram.com/v21.0"
YT_API = "https://www.googleapis.com/youtube/v3"
WHOP_API = "https://api.whop.com/api/v1"


# ---------------------------------------------------------------------------
# Per-platform metric fetchers
# ---------------------------------------------------------------------------
def fetch_tiktok_stats(access_token: str, video_ids: List[str]) -> Dict[str, Dict]:
    """Fetch TikTok video statistics via /video/query/."""
    s = http_session(token=access_token,
                     extra_headers={"Content-Type": "application/json; charset=UTF-8"})
    out = {}
    # TikTok allows batch query (max 100 per request)
    for batch_start in range(0, len(video_ids), 100):
        batch = video_ids[batch_start:batch_start + 100]
        r = s.post(
            f"{TIKTOK_API}/video/query/",
            json={"filters": {"video_ids": batch}},
            timeout=30,
        )
        r.raise_for_status()
        j = r.json()
        for v in j.get("data", {}).get("videos", []):
            out[v["id"]] = {
                "views": v.get("view_count", 0),
                "likes": v.get("like_count", 0),
                "comments": v.get("comment_count", 0),
                "shares": v.get("share_count", 0),
                "saves": v.get("save_count") or v.get("favorite_count", 0),
                "reach": v.get("reach_count") or v.get("view_count", 0),
                "create_time": v.get("create_time"),
            }
    return out


def fetch_instagram_stats(access_token: str, media_ids: List[str]) -> Dict[str, Dict]:
    """Fetch IG Reels insights via /media_id/insights."""
    s = http_session()
    out = {}
    for mid in media_ids:
        r = s.get(
            f"{GRAPH_API}/{mid}/insights",
            params={
                "metric": "views,likes,comments,saves,shares,follows,"
                          "profile_visits,reach,total_views,video_views,"
                          "clips_replays_count",
                "access_token": access_token,
            },
            timeout=30,
        )
        if r.status_code != 200:
            log.warning(f"IG insights for {mid} failed: {r.status_code} {r.text[:200]}")
            continue
        j = r.json()
        flat = {}
        for item in j.get("data", []):
            name = item.get("name")
            vals = item.get("values", [])
            flat[name] = vals[0].get("value", 0) if vals else 0
        out[mid] = {
            "views": flat.get("total_views") or flat.get("video_views") or flat.get("views", 0),
            "likes": flat.get("likes", 0),
            "comments": flat.get("comments", 0),
            "shares": flat.get("shares", 0),
            "saves": flat.get("saves", 0),
            "follows": flat.get("follows", 0),
            "reach": flat.get("reach", 0),
            "replays": flat.get("clips_replays_count", 0),
        }
    return out


def fetch_youtube_stats(youtube, video_ids: List[str]) -> Dict[str, Dict]:
    """Fetch YT video stats (viewCount, likeCount, commentCount)."""
    out = {}
    # videos.list supports up to 50 IDs per call
    for i in range(0, len(video_ids), 50):
        batch = video_ids[i:i + 50]
        r = youtube.videos().list(
            part="statistics,snippet,contentDetails",
            id=",".join(batch),
        ).execute()
        for item in r.get("items", []):
            stats = item.get("statistics", {})
            content = item.get("contentDetails", {})
            snippet = item.get("snippet", {})
            out[item["id"]] = {
                "views": int(stats.get("viewCount", 0)),
                "likes": int(stats.get("likeCount", 0)),
                "comments": int(stats.get("commentCount", 0)),
                # duration comes as ISO 8601 (e.g. "PT20S")
                "duration_iso": content.get("duration"),
                "title": snippet.get("title"),
                "published_at": snippet.get("publishedAt"),
            }
    return out


def fetch_youtube_analytics(youtube, video_ids: List[str],
                             start_date: str, end_date: str) -> Dict[str, Dict]:
    """Fetch YouTube Analytics (AVD, watch time). Requires YPP access.
    Returns dict video_id -> metrics."""
    if not video_ids:
        return {}
    try:
        r = youtube.reports().query(
            ids="channel==MINE",
            startDate=start_date,
            endDate=end_date,
            metrics="views,estimatedMinutesWatched,averageViewDuration,likes,dislikes,comments,shares,subscribersGained",
            filters=f"video=={','.join(video_ids[:50])}",  # 50 max in filter
        ).execute()
        # rows: list of [video_id, views, minutes_watched, avg_view_dur, ...]
        out = {}
        for row in r.get("rows", []):
            out[row[0]] = {
                "views": int(row[1]) if len(row) > 1 else 0,
                "minutes_watched": int(row[2]) if len(row) > 2 else 0,
                "avg_view_duration_sec": float(row[3]) if len(row) > 3 else 0,
                "likes": int(row[4]) if len(row) > 4 else 0,
                "dislikes": int(row[5]) if len(row) > 5 else 0,
                "comments": int(row[6]) if len(row) > 6 else 0,
                "shares": int(row[7]) if len(row) > 7 else 0,
                "subscribers_gained": int(row[8]) if len(row) > 8 else 0,
            }
        return out
    except Exception as e:
        log.warning(f"YT analytics failed (need YPP + scope youtube.readonly): {e}")
        return {}


def fetch_whop_submissions(user_token: str,
                            bounty_ids: List[str]) -> Dict[str, Dict]:
    """Fetch Whop bounty submissions to track approval + payout."""
    s = http_session(token=user_token,
                     extra_headers={"Api-Version-Date": "2026-09-11"})
    out = {}
    for bid in bounty_ids:
        r = s.get(f"{WHOP_API}/bounty_submissions",
                  params={"bounty_id": bid}, timeout=30)
        if r.status_code != 200:
            log.warning(f"Whop submissions for {bid} failed: {r.status_code}")
            continue
        j = r.json()
        for sub in j.get("data", []):
            sub_id = sub.get("id")
            out[sub_id] = {
                "bounty_id": bid,
                "status": sub.get("status"),  # submitted/approved/denied
                "payout_amount": sub.get("gross_reward_amount") or
                                  sub.get("gross_paid_out_amount"),
                "currency": sub.get("reward_currency", "USD"),
                "submitted_at": sub.get("submitted_at"),
                "decided_at": sub.get("decided_at"),
                "deliverable": sub.get("deliverable", {}),
            }
    return out


# ---------------------------------------------------------------------------
# Aggregator: pulls everything for tracked videos
# ---------------------------------------------------------------------------
def pull_all(videos_index: List[Dict[str, Any]],
             full: bool = False,
             days_window: int = 30) -> Dict[str, Any]:
    """
    videos_index: list of {video_id, platform, bounty_id, duration_sec,
                          published_at, file_path}
    Returns full analytics dict.
    """
    state = state_load()
    last_pull_ts = state.get("last_analytics_pull", {}).get("ts", 0)

    # Filter videos that need refreshing (or all if full)
    now = time.time()
    cutoff = now - days_window * 86400
    videos_to_pull = []
    for v in videos_index:
        if full:
            videos_to_pull.append(v)
            continue
        published_ts = v.get("published_ts", 0) or 0
        if published_ts > cutoff or published_ts > last_pull_ts:
            videos_to_pull.append(v)

    log.info(f"Pulling analytics for {len(videos_to_pull)} videos "
             f"(total tracked: {len(videos_index)})")

    # Group by platform
    tiktok_ids = [v["video_id"] for v in videos_to_pull if v["platform"] == "tiktok"]
    ig_ids = [v["video_id"] for v in videos_to_pull if v["platform"] == "instagram"]
    yt_ids = [v["video_id"] for v in videos_to_pull if v["platform"] == "youtube"]
    bounty_ids = list({v["bounty_id"] for v in videos_to_pull
                       if v.get("bounty_id")})

    results = {"date_utc": datetime.now(timezone.utc).isoformat(),
               "platforms": {}, "videos": {}}

    # TikTok
    if tiktok_ids:
        token = os.environ.get("TIKTOK_ACCESS_TOKEN")
        if token:
            try:
                results["platforms"]["tiktok"] = fetch_tiktok_stats(token, tiktok_ids)
            except Exception as e:
                log.error(f"TikTok pull failed: {e}")
        else:
            log.warning("TIKTOK_ACCESS_TOKEN not set — skipping TikTok")

    # Instagram
    if ig_ids:
        token = os.environ.get("IG_ACCESS_TOKEN")
        if token:
            try:
                results["platforms"]["instagram"] = fetch_instagram_stats(token, ig_ids)
            except Exception as e:
                log.error(f"Instagram pull failed: {e}")
        else:
            log.warning("IG_ACCESS_TOKEN not set — skipping Instagram")

    # YouTube
    if yt_ids:
        try:
            from publish_youtube import get_authenticated_service  # type: ignore
            yt = get_authenticated_service()
            results["platforms"]["youtube"] = fetch_youtube_stats(yt, yt_ids)
            today = datetime.now(timezone.utc).date()
            start = (today - timedelta(days=days_window)).isoformat()
            end = today.isoformat()
            results["platforms"]["youtube_analytics"] = fetch_youtube_analytics(
                yt, yt_ids, start, end)
        except Exception as e:
            log.error(f"YouTube pull failed: {e}")

    # Whop
    if bounty_ids:
        token = os.environ.get("WHOP_USER_TOKEN")
        if token:
            try:
                results["platforms"]["whop"] = fetch_whop_submissions(token, bounty_ids)
            except Exception as e:
                log.error(f"Whop pull failed: {e}")
        else:
            log.warning("WHOP_USER_TOKEN not set — skipping Whop")

    # Compute per-video aggregated metrics
    for v in videos_to_pull:
        vid = v["video_id"]
        platform = v["platform"]
        platform_stats = results["platforms"].get(platform, {})
        vstats = platform_stats.get(vid, {})
        # compute derived metrics
        duration = v.get("duration_sec", 0)
        views = vstats.get("views", 0)
        reach = vstats.get("reach", 0) or views
        likes = vstats.get("likes", 0)
        comments = vstats.get("comments", 0)
        shares = vstats.get("shares", 0)
        saves = vstats.get("saves", 0)
        avg_view_dur = vstats.get("avg_view_duration_sec", 0) or \
                       (vstats.get("minutes_watched", 0) * 60 / max(views, 1))

        view_rate = (views / reach) * 100 if reach else 0
        avd_pct = (avg_view_dur / duration * 100) if duration else 0
        share_rate = (shares / views * 100) if views else 0
        save_rate = (saves / views * 100) if views else 0
        engagement_rate = ((likes + comments + shares + saves) / views * 100) if views else 0

        results["videos"][f"{platform}:{vid}"] = {
            "platform": platform,
            "video_id": vid,
            "url": v.get("url"),
            "title": v.get("title"),
            "bounty_id": v.get("bounty_id"),
            "duration_sec": duration,
            "published_at": v.get("published_at"),
            "raw_stats": vstats,
            "computed": {
                "views": views,
                "reach": reach,
                "view_rate_pct": round(view_rate, 2),
                "avd_pct": round(avd_pct, 2),
                "share_rate_pct": round(share_rate, 2),
                "save_rate_pct": round(save_rate, 2),
                "engagement_rate_pct": round(engagement_rate, 2),
            },
            "benchmarks_target": {
                "view_rate_pct_min": 85.0,
                "avd_pct_min": 70.0,
                "share_rate_pct_min": 1.7,
                "save_rate_pct_min": 2.0,
            },
            "meets_target": {
                "view_rate": view_rate >= 85.0,
                "avd": avd_pct >= 70.0,
                "share_rate": share_rate >= 1.7,
                "save_rate": save_rate >= 2.0,
            },
        }

    state["last_analytics_pull"] = {"ts": now,
                                     "n_videos": len(videos_to_pull)}
    state_save(state)
    return results


# ---------------------------------------------------------------------------
# Output writers
# ---------------------------------------------------------------------------
def write_csv(analytics: Dict[str, Any], out_path: Path) -> None:
    """Write flat CSV: one row per video."""
    out_path.parent.mkdir(parents=True, exist_ok=True)
    rows = []
    for key, v in analytics.get("videos", {}).items():
        c = v.get("computed", {})
        m = v.get("meets_target", {})
        rows.append({
            "date_utc": analytics.get("date_utc"),
            "platform": v.get("platform"),
            "video_id": v.get("video_id"),
            "title": (v.get("title") or "")[:80],
            "duration_sec": v.get("duration_sec"),
            "published_at": v.get("published_at"),
            "bounty_id": v.get("bounty_id"),
            "views": c.get("views"),
            "reach": c.get("reach"),
            "view_rate_pct": c.get("view_rate_pct"),
            "avd_pct": c.get("avd_pct"),
            "share_rate_pct": c.get("share_rate_pct"),
            "save_rate_pct": c.get("save_rate_pct"),
            "engagement_rate_pct": c.get("engagement_rate_pct"),
            "meets_view_rate": m.get("view_rate"),
            "meets_avd": m.get("avd"),
            "meets_share_rate": m.get("share_rate"),
            "meets_save_rate": m.get("save_rate"),
            "url": v.get("url"),
        })
    fieldnames = list(rows[0].keys()) if rows else []
    with open(out_path, "w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fieldnames)
        w.writeheader()
        for r in rows:
            w.writerow(r)
    # Append to history CSV
    history_path = DATA_DIR / "analytics_history.csv"
    if history_path.exists():
        with open(history_path, "a", encoding="utf-8", newline="") as f:
            w = csv.DictWriter(f, fieldnames=fieldnames)
            for r in rows:
                w.writerow(r)
    else:
        with open(history_path, "w", encoding="utf-8", newline="") as f:
            w = csv.DictWriter(f, fieldnames=fieldnames)
            w.writeheader()
            for r in rows:
                w.writerow(r)


# ---------------------------------------------------------------------------
# Videos index management
# ---------------------------------------------------------------------------
def load_videos_index() -> List[Dict[str, Any]]:
    """Load the videos.json index (built by add + publish scripts)."""
    path = DATA_DIR / "videos_index.json"
    if not path.exists():
        return []
    return read_json(path)


def save_videos_index(items: List[Dict[str, Any]]) -> None:
    path = DATA_DIR / "videos_index.json"
    write_json(items, path)


def add_video_to_index(platform: str, video_id: str,
                       url: Optional[str] = None,
                       title: Optional[str] = None,
                       bounty_id: Optional[str] = None,
                       duration_sec: Optional[float] = None,
                       file_path: Optional[str] = None,
                       published_at: Optional[str] = None) -> None:
    """Add a video to the tracking index. Used by publish_* scripts."""
    items = load_videos_index()
    # dedup by platform:video_id
    for it in items:
        if it["platform"] == platform and it["video_id"] == video_id:
            log.info(f"Updating existing entry {platform}:{video_id}")
            it.update({"url": url, "title": title, "bounty_id": bounty_id,
                       "duration_sec": duration_sec, "file_path": file_path,
                       "published_at": published_at or it.get("published_at"),
                       "published_ts": time.time()})
            save_videos_index(items)
            return
    items.append({
        "platform": platform, "video_id": video_id, "url": url, "title": title,
        "bounty_id": bounty_id, "duration_sec": duration_sec,
        "file_path": file_path, "published_at": published_at,
        "published_ts": time.time(),
    })
    save_videos_index(items)


# ---------------------------------------------------------------------------
# Summary printer
# ---------------------------------------------------------------------------
def print_summary(analytics: Dict[str, Any]) -> None:
    """Pretty print summary of all videos + their target achievement."""
    videos = analytics.get("videos", {})
    if not videos:
        print("No videos tracked yet.")
        return
    print(f"\n=== Analytics Summary ({analytics.get('date_utc')}) ===")
    print(f"{'platform':<11} {'video_id':<14} "
          f"{'views':>9} {'vr%':>6} {'avd%':>6} "
          f"{'sh%':>6} {'sv%':>6} {'met':<12}")
    print("-" * 80)
    for key, v in videos.items():
        c = v.get("computed", {})
        m = v.get("meets_target", {})
        met = sum(1 for x in m.values() if x)
        total = len(m)
        status = f"{met}/{total}"
        print(f"{v['platform']:<11} {v['video_id'][:12]:<14} "
              f"{c.get('views', 0):>9} "
              f"{c.get('view_rate_pct', 0):>5.1f}% "
              f"{c.get('avd_pct', 0):>5.1f}% "
              f"{c.get('share_rate_pct', 0):>5.2f}% "
              f"{c.get('save_rate_pct', 0):>5.2f}% "
              f"{status:<12}")


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------
def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)

    p_pull = sub.add_parser("pull", help="Fetch latest analytics")
    p_pull.add_argument("--full", action="store_true",
                       help="Refetch everything (not just recent)")
    p_pull.add_argument("--days", type=int, default=30,
                        help="Days back to consider (default 30)")

    sub.add_parser("summary", help="Print last-pulled summary")

    p_add = sub.add_parser("add", help="Add a video to the tracking index")
    p_add.add_argument("--platform", required=True,
                       choices=["tiktok", "instagram", "youtube"])
    p_add.add_argument("--video-id", required=True)
    p_add.add_argument("--url", default=None)
    p_add.add_argument("--title", default=None)
    p_add.add_argument("--bounty-id", default=None)
    p_add.add_argument("--duration", type=float, default=None,
                       help="Video duration in seconds")
    p_add.add_argument("--file", default=None)
    p_add.add_argument("--published-at", default=None,
                       help="ISO 8601 datetime when published")

    p_list = sub.add_parser("list", help="List tracked videos")

    args = ap.parse_args()

    if args.cmd == "add":
        add_video_to_index(
            platform=args.platform, video_id=args.video_id,
            url=args.url, title=args.title, bounty_id=args.bounty_id,
            duration_sec=args.duration, file_path=args.file,
            published_at=args.published_at,
        )
        print(f"✓ Added {args.platform}:{args.video_id}")
        return

    if args.cmd == "list":
        items = load_videos_index()
        for it in items:
            print(f"{it['platform']:<11} {it['video_id']:<14} "
                  f"bounty={it.get('bounty_id') or '-':<20} "
                  f"dur={it.get('duration_sec') or 0:.0f}s "
                  f"url={it.get('url') or '-'}")
        return

    if args.cmd == "pull":
        items = load_videos_index()
        if not items:
            print("No videos tracked yet. Use `add` first.")
            return
        result = pull_all(items, full=args.full, days_window=args.days)
        date_str = datetime.now(timezone.utc).strftime("%Y-%m-%d")
        json_path = DATA_DIR / f"analytics_{date_str}.json"
        csv_path = DATA_DIR / f"analytics_{date_str}.csv"
        write_json(result, json_path)
        write_csv(result, csv_path)
        state_set("analytics_last_pull", {"ts": time.time(),
                                          "n_videos": len(result.get("videos", {}))})
        print_summary(result)
        print(f"\n✓ JSON: {json_path}")
        print(f"✓ CSV:  {csv_path}")
        return

    if args.cmd == "summary":
        # Load last-pulled analytics JSON
        items = load_videos_index()
        if not items:
            print("No videos tracked.")
            return
        result = pull_all(items, full=True, days_window=30)
        print_summary(result)
        return


if __name__ == "__main__":
    main()
