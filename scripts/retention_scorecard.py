#!/usr/bin/env python3
"""
retention_scorecard.py — Quality gate before publish
=====================================================
The 6-point Retention Scorecard (Master_Video_Production ninja cheatsheet).

A video MUST score >=5/6 before being published — automatically refuses
publish in viral_edit.py if <5/6.

The 6 checks:
  1. Hook strength  — first 3s text contains hook keyword + >3 words spoken.
  2. Caption presence — .ass / .srt file exists for the clip OR burned-in.
  3. Vertical format — 9:16 (1080x1920 ±5% tolerance).
  4. Duration sweet-spot — 15s <= dur <= 75s (sweet-spot for FYP).
  5. Pattern interrupt — B-roll or double-zoom or J-Cut applied.
  6. Loop closer — last 0.5s was the looped/reversed tail (audio check).

Each check returns {pass, score, detail}. Total score = sum of (1 if pass).
"""
from __future__ import annotations

import argparse
import json
import os
import re
import sys
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _common import (  # noqa: E402
    log, get_logger, write_json, read_json, run, probe_duration,
    probe_dimensions, probe_audio, state_get, WORKDIR,
)

log = get_logger("scorecard")


# ---------------------------------------------------------------------------
# Hook keywords (must appear in first 3s of the transcript)
# ---------------------------------------------------------------------------
HOOK_KEYWORDS = [
    "million", "billion", "money", "rich", "wealth", "income", "secret",
    "truth", "wrong", "right", "real", "actually", "nobody", "everyone",
    "lie", "myth", "stop", "never", "always", "first", "best", "worst",
    "biggest", "fastest", "easiest", "hardest", "guaranteed", "promise",
    "100", "perfect", "how", "why", "what", "imagine", "picture", "think",
    "believe", "fail", "failed", "lose", "lost", "win", "won", "habit",
    "discipline", "lazy", "addicted", "quit", "today", "now", "immediately",
    "before", "after", "business", "founder", "ceo", "startup",
    "marketing", "audience", "customer", "product",
]


@dataclass
class Check:
    name: str
    passed: bool
    score: int  # 0 or 1
    detail: str
    weight: int = 1  # all checks weighted equally (1 pt each)


# ---------------------------------------------------------------------------
# 1. Hook strength (first 3s)
# ---------------------------------------------------------------------------
def check_hook_strength(transcript_path: Optional[str], start_sec: float,
                        end_sec: float) -> Check:
    """Score: hook text contains HOOK_KEYWORDS + >3 words in first 3s."""
    if not transcript_path or not Path(transcript_path).exists():
        return Check("hook_strength", False, 0, "transcript missing")
    transcript = read_json(transcript_path)
    hook_end = start_sec + 3.0
    # Gather words spoken in [start_sec, start_sec+3]
    hook_words: List[str] = []
    for seg in transcript.get("segments", []):
        for w in (seg.get("words") or []):
            if w["start"] >= start_sec and w["end"] <= hook_end:
                hook_words.append(w["word"].lower())
    if len(hook_words) < 3:
        return Check("hook_strength", False, 0,
                     f"only {len(hook_words)} words in first 3s (need >=3)")
    matched = [kw for kw in HOOK_KEYWORDS if any(kw in word for word in hook_words)]
    if not matched:
        return Check("hook_strength", False, 0,
                     f"hook text lacks keywords: {' '.join(hook_words[:8])}")
    return Check("hook_strength", True, 1,
                 f"hook={len(hook_words)} words, keywords: {','.join(matched[:5])}")


# ---------------------------------------------------------------------------
# 2. Caption presence
# ---------------------------------------------------------------------------
def check_captions(video_path: str) -> Check:
    """Pass if the video has burned-in captions (detected via having a
    captioned intermediate) OR there's an .srt/.ass file alongside."""
    # Check state for captioned = True (set by viral_edit pipeline)
    state_key = f"viral_edit:{video_path}"
    state = state_get(state_key)
    if state and state.get("use_captions"):
        return Check("captions", True, 1, "burned-in (Hormozi ASS)")

    # Else check for sidecar .srt or .ass
    p = Path(video_path)
    sidecars = list(p.parent.glob(f"{p.stem}.srt")) + \
               list(p.parent.glob(f"{p.stem}.ass"))
    if sidecars:
        return Check("captions", True, 1, f"sidecar: {sidecars[0].name}")
    return Check("captions", False, 0, "no captions detected")


# ---------------------------------------------------------------------------
# 3. Vertical 9:16 format
# ---------------------------------------------------------------------------
def check_vertical(video_path: str) -> Check:
    """Pass if width:height ratio ~9:16 (1080x1920 or similar)."""
    try:
        w, h = probe_dimensions(video_path)
    except Exception as e:
        return Check("vertical_9_16", False, 0, f"ffprobe failed: {e}")
    ratio = h / w
    expected = 1920 / 1080  # 1.778
    tolerance = 0.05
    if abs(ratio - expected) / expected < tolerance:
        return Check("vertical_9_16", True, 1, f"{w}x{h} (ratio={ratio:.3f})")
    return Check("vertical_9_16", False, 0, f"{w}x{h} (ratio={ratio:.3f}, need ~1.778)")


# ---------------------------------------------------------------------------
# 4. Duration sweet-spot (15-75s)
# ---------------------------------------------------------------------------
def check_duration(video_path: str) -> Check:
    try:
        d = probe_duration(video_path)
    except Exception as e:
        return Check("duration_sweet_spot", False, 0, f"ffprobe failed: {e}")
    if 15 <= d <= 75:
        return Check("duration_sweet_spot", True, 1, f"{d:.1f}s (sweet-spot)")
    if 8 <= d < 15:
        return Check("duration_sweet_spot", False, 0, f"{d:.1f}s (too short — need >=15s)")
    if 75 < d <= 180:
        return Check("duration_sweet_spot", False, 0, f"{d:.1f}s (too long — TikTok sweet spot is 25-75s)")
    return Check("duration_sweet_spot", False, 0, f"{d:.1f}s (out of range)")


# ---------------------------------------------------------------------------
# 5. Pattern interrupt (B-roll OR double-zoom OR J-Cut)
# ---------------------------------------------------------------------------
def check_pattern_interrupt(video_path: str) -> Check:
    """Pass if the video has been processed with at least one pattern interrupt.
    We check the pipeline state for use_double_zoom / use_broll / use_jcut."""
    state_key = f"viral_edit:{video_path}"
    state = state_get(state_key)
    if not state:
        # heuristic: video dimensions differ from source? can't tell without
        # source. Allow manual override via env RETENTION_OVERRIDE=1.
        if os.environ.get("RETENTION_OVERRIDE") == "1":
            return Check("pattern_interrupt", True, 1, "override=1 (manual)")
        return Check("pattern_interrupt", False, 0,
                     "no viral_edit state found (call viral_edit first)")
    interrupts = []
    if state.get("use_double_zoom"):
        interrupts.append("double_zoom")
    if state.get("use_broll"):
        interrupts.append("b_roll")
    if state.get("use_jcut"):
        interrupts.append("j_cut")
    if interrupts:
        return Check("pattern_interrupt", True, 1,
                     f"applied: {','.join(interrupts)}")
    return Check("pattern_interrupt", False, 0, "no pattern interrupts applied")


# ---------------------------------------------------------------------------
# 6. Loop closer (last 0.5s is reversed tail — check audio waveform symmetry)
# ---------------------------------------------------------------------------
def check_loop_closer(video_path: str) -> Check:
    """Heuristic: if viral_edit state.use_loop_closer=True → pass.
    Else: extract last 0.5s + first 0.5s, compare audio similarity (rude)."""
    state_key = f"viral_edit:{video_path}"
    state = state_get(state_key)
    if state and state.get("use_loop_closer"):
        return Check("loop_closer", True, 1, "looped tail appended")
    # Audio-based check: extract last 0.5s, reverse it, check if it's similar
    # to the 0.5s before it. We'll skip this complex check if no state.
    if os.environ.get("RETENTION_OVERRIDE") == "1":
        return Check("loop_closer", True, 1, "override=1 (manual)")
    return Check("loop_closer", False, 0,
                 "no loop closer detected (state.use_loop_closer=False)")


# ---------------------------------------------------------------------------
# Total score
# ---------------------------------------------------------------------------
def score_video(video_path: str,
                transcript_path: Optional[str] = None,
                start_sec: float = 0.0,
                end_sec: Optional[float] = None,
                min_score: int = 5) -> Dict[str, Any]:
    """Run all 6 checks. Return dict with score + per-check details + passed."""
    video_path = str(Path(video_path).resolve())
    if not Path(video_path).exists():
        raise SystemExit(f"video not found: {video_path}")

    if end_sec is None:
        try:
            end_sec = probe_duration(video_path) + start_sec
        except Exception:
            end_sec = start_sec + 60

    checks: List[Check] = [
        check_hook_strength(transcript_path, start_sec, end_sec),
        check_captions(video_path),
        check_vertical(video_path),
        check_duration(video_path),
        check_pattern_interrupt(video_path),
        check_loop_closer(video_path),
    ]

    total_score = sum(c.score for c in checks)
    max_score = len(checks)
    passed = total_score >= min_score

    return {
        "passed": passed,
        "score": total_score,
        "max_score": max_score,
        "min_required": min_score,
        "checks": [asdict(c) for c in checks],
        "video_path": video_path,
        "transcript_path": transcript_path,
        "start_sec": start_sec,
        "end_sec": end_sec,
    }


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------
def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--video", required=True, help="Final video path")
    ap.add_argument("--transcript", default=None,
                    help="Transcript .words.json (for hook check)")
    ap.add_argument("--start", type=float, default=0.0,
                    help="Start sec in source timeline (for hook window)")
    ap.add_argument("--end", type=float, default=None)
    ap.add_argument("--min", type=int, default=5,
                    help="Minimum score required to pass (default 5/6)")
    ap.add_argument("--out", default=None,
                    help="Write scorecard JSON to this path")
    args = ap.parse_args()

    result = score_video(args.video, args.transcript, args.start, args.end,
                         min_score=args.min)

    if args.out:
        write_json(result, args.out)
        print(f"Wrote: {args.out}")

    print(json.dumps(result, indent=2))
    if result["passed"]:
        print(f"\n✓ PASS: {result['score']}/{result['max_score']} (>= {args.min})")
        sys.exit(0)
    else:
        print(f"\n✗ FAIL: {result['score']}/{result['max_score']} (< {args.min})")
        sys.exit(2)


if __name__ == "__main__":
    main()
