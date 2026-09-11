#!/usr/bin/env python3
"""
download_source.py — Layer 1 of the open-source stack
=====================================================
Download source videos (podcasts, interviews, etc.) via yt-dlp.

Key capabilities:
  - Fetch metadata first (title, duration, uploader) without downloading.
  - Download full video OR a target time-range segment (--segment START:END).
  - Auto-write auto-subs (en/ar) if available, convert to SRT.
  - Output JSON manifest {url, video_id, title, duration_sec, file_path,
    subtitles, downloaded_at}.
  - Idempotent: re-running with same video_id + skip-existing=true reuses file.

yt-dlp reference: https://github.com/yt-dlp/yt-dlp (MIT licence).

Usage:
    python3 download_source.py --url "https://youtu.be/XXXX" --out download/
    python3 download_source.py --url "URL" --segment 600:660 --out dl.mp4
    python3 download_source.py --url "URL" --metadata-only
"""
from __future__ import annotations

import argparse
import json
import os
import shutil
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, Optional, Tuple

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _common import (  # noqa: E402
    run, write_json, read_json, get_logger, state_set, state_get,
    PROJECT_ROOT, WORKDIR,
)

try:
    import yt_dlp  # type: ignore
    YT_DLP_VERSION = yt_dlp.version.__version__
except Exception:
    YT_DLP_VERSION = "unknown (not installed)"

log = get_logger("download_source")


# ---------------------------------------------------------------------------
# 1. Metadata fetch
# ---------------------------------------------------------------------------
def fetch_metadata(url: str) -> Dict[str, Any]:
    """Fetch video metadata without downloading. Uses yt-dlp's extract_info."""
    ydl_opts = {
        "quiet": True,
        "skip_download": True,
        "noplaylist": True,
        "no_warnings": True,
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=False)

    # Required fields
    return {
        "url": url,
        "video_id": info.get("id"),
        "title": info.get("title"),
        "uploader": info.get("uploader") or info.get("channel"),
        "duration_sec": info.get("duration"),
        "upload_date": info.get("upload_date"),
        "view_count": info.get("view_count"),
        "description": (info.get("description") or "")[:5000],
        "automatic_captions": list((info.get("automatic_captions") or {}).keys())[:30],
        "thumbnail": info.get("thumbnail"),
        "extractor": info.get("extractor_key") or info.get("extractor"),
    }


# ---------------------------------------------------------------------------
# 2. Full download
# ---------------------------------------------------------------------------
def download_full(url: str, out_dir: str,
                  fmt: str = "bestvideo[height<=1080]+bestaudio/best[height<=1080]/best",
                  write_subs: bool = True,
                  sub_lang: str = "en,ar",
                  skip_existing: bool = True) -> Dict[str, Any]:
    """Download full video + auto-subs as SRT. Returns manifest."""
    out_dir_p = Path(out_dir)
    out_dir_p.mkdir(parents=True, exist_ok=True)
    out_tmpl = str(out_dir_p / "%(id)s.%(ext)s")

    # If we already have the metadata, derive video_id for skip-existing
    meta = fetch_metadata(url)
    vid = meta["video_id"]
    expected_mp4 = out_dir_p / f"{vid}.mp4"
    expected_srt_en = out_dir_p / f"{vid}.en.srt"

    if skip_existing and expected_mp4.exists():
        log.info(f"Skip-existing: reusing {expected_mp4}")
        return {
            **meta,
            "file_path": str(expected_mp4),
            "subtitles": [str(expected_srt_en)] if expected_srt_en.exists() else [],
            "downloaded_at": datetime.now(timezone.utc).isoformat(),
            "method": "reused",
        }

    ydl_opts = {
        "format": fmt,
        "merge_output_format": "mp4",
        "outtmpl": out_tmpl,
        "noplaylist": True,
        "quiet": False,
        "no_warnings": False,
        "writethumbnail": False,
    }
    if write_subs:
        ydl_opts.update({
            "writeautomaticsub": True,
            "sublangs": sub_lang.split(","),
            "subtitlesformat": "srt",
            "convertsubtitles": "srt",
        })

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

    # locate outputs
    mp4s = sorted(out_dir_p.glob("*.mp4"), key=lambda p: p.stat().st_mtime, reverse=True)
    if not mp4s:
        raise RuntimeError("yt-dlp produced no mp4")
    mp4 = mp4s[0]
    srts = sorted(out_dir_p.glob(f"{vid}*.srt"))

    manifest = {
        **meta,
        "file_path": str(mp4),
        "subtitles": [str(s) for s in srts],
        "downloaded_at": datetime.now(timezone.utc).isoformat(),
        "method": "yt-dlp full",
    }
    state_set(f"download:{vid}", manifest)
    return manifest


# ---------------------------------------------------------------------------
# 3. Segment download (efficient — uses yt-dlp internal section)
# ---------------------------------------------------------------------------
def download_segment(url: str, start_sec: float, end_sec: float,
                     out_path: str,
                     fmt: str = "bestvideo[height<=1080]+bestaudio/best[height<=1080]/best") -> Dict[str, Any]:
    """
    Download a sub-segment of the video.

    Strategy: use yt-dlp --download-sections "*START-END" which fetches only
    the requested byte-range from supported sites (YouTube, etc.). For
    unsupported sites, falls back to full download + ffmpeg trim.
    """
    out_p = Path(out_path)
    out_p.parent.mkdir(parents=True, exist_ok=True)

    section_spec = f"*{start_sec}-{end_sec}"
    out_tmpl = str(out_p.with_suffix(".%(ext)s"))

    ydl_opts = {
        "format": fmt,
        "merge_output_format": "mp4",
        "outtmpl": out_tmpl,
        "noplaylist": True,
        "download_ranges": yt_dlp.utils._config_section_or_range(section_spec) \
            if hasattr(yt_dlp.utils, "_config_section_or_range") else None,
        "force_key_frames_at_cuts": True,  # for accurate trim
    }
    # Use the official --download-sections syntax
    if ydl_opts["download_ranges"] is None:
        # modern API: pass list of (start, end) tuples
        ydl_opts["download_ranges"] = [{"start_time": start_sec, "end_time": end_sec}]

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

    # locate the produced file
    produced = sorted(out_p.parent.glob(f"{out_p.stem}*.mp4"),
                      key=lambda p: p.stat().st_mtime, reverse=True)
    if not produced:
        raise RuntimeError("yt-dlp segment download produced no mp4")
    # rename to canonical name if needed
    if produced[0] != out_p:
        shutil.move(str(produced[0]), str(out_p))

    meta = fetch_metadata(url)
    manifest = {
        "url": url,
        "video_id": meta["video_id"],
        "title": meta["title"],
        "uploader": meta["uploader"],
        "segment_start_sec": start_sec,
        "segment_end_sec": end_sec,
        "segment_duration_sec": end_sec - start_sec,
        "file_path": str(out_p),
        "downloaded_at": datetime.now(timezone.utc).isoformat(),
        "method": "yt-dlp segment",
    }
    state_set(f"download_segment:{meta['video_id']}:{int(start_sec)}", manifest)
    return manifest


# ---------------------------------------------------------------------------
# 4. Alternative: full download + ffmpeg trim (for sites without section API)
# ---------------------------------------------------------------------------
def download_then_trim(url: str, start_sec: float, end_sec: float,
                       out_path: str, out_dir: str = None) -> Dict[str, Any]:
    """Fallback path: full download → ffmpeg trim. Used when yt-dlp section
    download is unsupported or fails."""
    out_dir = out_dir or str(WORKDIR / "downloads")
    full = download_full(url, out_dir)
    trim_video(full["file_path"], start_sec, end_sec, out_path)
    manifest = {
        **{k: v for k, v in full.items() if k != "file_path"},
        "segment_start_sec": start_sec,
        "segment_end_sec": end_sec,
        "segment_duration_sec": end_sec - start_sec,
        "file_path": str(out_path),
        "method": "full-download + ffmpeg trim",
    }
    state_set(f"download_segment:{full['video_id']}:{int(start_sec)}", manifest)
    return manifest


# ---------------------------------------------------------------------------
# 5. ffmpeg trim helper
# ---------------------------------------------------------------------------
def trim_video(src: str, start_sec: float, end_sec: float, out_path: str) -> None:
    """Accurate ffmpeg trim. Re-encodes to ensure key-frames align."""
    duration = end_sec - start_sec
    run([
        "ffmpeg", "-y", "-ss", f"{start_sec:.3f}", "-i", src,
        "-t", f"{duration:.3f}",
        "-c:v", "libx264", "-preset", "fast", "-crf", "20",
        "-pix_fmt", "yuv420p",
        "-c:a", "aac", "-b:a", "192k",
        "-avoid_negative_ts", "0",
        out_path,
    ])


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------
def _parse_segment(spec: str) -> Tuple[float, float]:
    if ":" in spec:
        h, m, s = spec.split(":")
        return float(h) * 3600 + float(m) * 60 + float(s), 0  # only single ts
    if "-" not in spec:
        raise SystemExit("--segment must be START-END (e.g. 600-660 or 10:00-11:00)")
    start_s, end_s = spec.split("-", 1)

    def to_sec(s: str) -> float:
        if ":" in s:
            parts = s.split(":")
            if len(parts) == 2:
                return float(parts[0]) * 60 + float(parts[1])
            return float(parts[0]) * 3600 + float(parts[1]) * 60 + float(parts[2])
        return float(s)

    return to_sec(start_s), to_sec(end_s)


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--url", required=True, help="Source URL (YouTube, etc.)")
    ap.add_argument("--out", default="download/", help="Output dir or file path")
    ap.add_argument("--segment", default=None,
                    help="START-END (seconds or HH:MM:SS-HH:MM:SS). "
                         "Triggers yt-dlp section download.")
    ap.add_argument("--metadata-only", action="store_true",
                    help="Only fetch metadata, do not download")
    ap.add_argument("--no-subs", action="store_true",
                    help="Skip writing auto-subs")
    ap.add_argument("--format", default=None,
                    help="Override yt-dlp -f format string")
    ap.add_argument("--manifest", default=None,
                    help="Path to write JSON manifest (default: <out>.manifest.json)")
    args = ap.parse_args()

    print(f"yt-dlp version: {YT_DLP_VERSION}")

    if args.metadata_only:
        meta = fetch_metadata(args.url)
        print(json.dumps(meta, indent=2, ensure_ascii=False))
        return

    fmt = args.format or "bestvideo[height<=1080]+bestaudio/best[height<=1080]/best"

    if args.segment:
        start, end = _parse_segment(args.segment)
        log.info(f"Downloading segment {start:.1f}-{end:.1f}s ({end-start:.1f}s)")
        # If out is a dir, build filename
        if args.out.endswith("/") or Path(args.out).is_dir():
            out_path = str(Path(args.out) / "segment.mp4")
        else:
            out_path = args.out
        manifest = download_segment(args.url, start, end, out_path, fmt=fmt)
    else:
        manifest = download_full(args.url, args.out,
                                 fmt=fmt, write_subs=not args.no_subs)

    manifest_path = args.manifest or (Path(manifest["file_path"]).with_suffix(".manifest.json"))
    write_json(manifest, manifest_path)
    print(f"\n✓ Download complete:")
    print(f"  File:      {manifest['file_path']}")
    print(f"  Manifest:  {manifest_path}")
    print(f"  Duration:  {manifest.get('duration_sec') or manifest.get('segment_duration_sec')}s")


if __name__ == "__main__":
    main()
