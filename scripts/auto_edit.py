#!/usr/bin/env python3
"""
auto_edit.py — Layer 3 of the open-source stack
=================================================
Automatic silence removal + viral segment detection.

Pipeline:
  1. Transcribe (uses transcribe.py)
  2. Remove silence/fillers via auto-editor (or librosa fallback)
  3. Detect candidate viral segments via simple sentiment + density heuristic:
       - Keyword hook: "money", "million", "secret", "wrong", "truth", "first",
         "stop", "never", "always", "how", "why", "money", "rich" (configurable)
       - High word-density (words/sec) > 3
       - Segment duration 25-75s (TikTok sweet spot)
       - Optional: low silence ratio (already stripped) → tight delivery
  4. For each candidate: emit {file, start, end, hook_text, score, reason}
  5. Top-K by score are exported as individual cut files (ffmpeg trim).

Outputs:
  - <base>.tight.mp4       — silence-stripped version of the source
  - <base>.cuts/            — directory of trimmed clips (one per candidate)
  - <base>.candidates.json  — list of detected viral candidates

Usage:
    python3 auto_edit.py input.mp4 --top-k 5 --out-dir auto_cuts/
    python3 auto_edit.py input.mp4 --transcript transcripts/x.words.json
"""
from __future__ import annotations

import argparse
import json
import os
import re
import shutil
import subprocess
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _common import (  # noqa: E402
    log, get_logger, write_json, read_json, run, probe_duration,
    state_set, state_get, WORKDIR, DATA_DIR,
)

log = get_logger("auto_edit")


# ---------------------------------------------------------------------------
# Default hook keywords (Hormozi-style virality triggers)
# ---------------------------------------------------------------------------
HOOK_KEYWORDS = [
    # Money / outcome
    "million", "billion", "money", "rich", "wealth", "income", "revenue",
    "profit", "dollars", "cash", "broke", "financial", "retire", "free",
    # Secrets / revelation
    "secret", "truth", "wrong", "right", "real", "actually", "nobody",
    "everyone", "lie", "lies", "myth", "stop", "never", "always",
    # Big claims
    "first", "best", "worst", "biggest", "fastest", "easiest", "hardest",
    "guaranteed", "promise", "100", "perfect",
    # Curiosity
    "how", "why", "what", "imagine", "picture", "think", "believe",
    # Numbers / specific
    "1", "2", "3", "five", "ten", "100", "1000",
    # Pain / transformation
    "fail", "failed", "lose", "lost", "win", "won", "habit", "discipline",
    "lazy", "addicted", "quit", "stop",
    # Time pressure
    "today", "now", "immediately", "before", "after", "yesterday", "tomorrow",
    # Whop / business
    "business", "founder", "ceo", "startup", "marketing", "audience",
    "customer", "product", "service",
]


# ---------------------------------------------------------------------------
# 1. Silence removal (auto-editor primary, librosa fallback)
# ---------------------------------------------------------------------------
def remove_silence_auto_editor(src: str, dst: str,
                                threshold_percent: int = 4,
                                frame_margin_sec: float = 0.2) -> str:
    """Cut silences using auto-editor (https://github.com/WyattFox/auto-editor).
    v29+ syntax: --margin uses seconds (e.g. 0.2s), --when-normal replaces --when-active.
    Default threshold = 4% peak volume, 0.2s margin.
    """
    Path(dst).parent.mkdir(parents=True, exist_ok=True)
    run([
        "auto-editor", src,
        "--edit", f"audio:{threshold_percent}%",
        "--margin", f"{frame_margin_sec}s",
        "--when-silent", "cut",
        "--when-normal", "nil",
        "-o", dst,
        "--no-open",
        "--export", "default",
    ])
    return dst


def remove_silence_librosa(src: str, dst: str,
                            silence_threshold_db: float = -40.0,
                            min_silence_ms: int = 500) -> str:
    """Fallback silence removal via librosa + ffmpeg.
    Detects non-silent regions, builds ffmpeg filter to keep them.
    """
    import librosa  # type: ignore
    import numpy as np

    # Extract audio
    audio_wav = str(WORKDIR / f"{Path(src).stem}_silence_audio.wav")
    run([
        "ffmpeg", "-y", "-i", src, "-vn", "-ac", "1", "-ar", "22050",
        audio_wav,
    ], check=True)

    y, sr = librosa.load(audio_wav, sr=22050, mono=True)
    # Frame-based RMS energy
    frame_length = int(sr * 0.030)  # 30ms
    hop = int(sr * 0.010)
    rms = librosa.feature.rms(y=y, frame_length=frame_length, hop_length=hop)[0]
    db = librosa.amplitude_to_db(rms, ref=1.0)

    # Find non-silent frames
    threshold = silence_threshold_db  # below = silent
    is_loud = db > threshold
    # Find runs of loud
    frames_per_sec = sr / hop
    min_silence_frames = int(min_silence_ms / 1000 * frames_per_sec)

    kept_segments: List[Tuple[float, float]] = []
    in_loud = False
    loud_start_frame = 0
    silence_start_frame = 0
    for i, loud in enumerate(is_loud):
        if loud and not in_loud:
            loud_start_frame = i
            in_loud = True
        elif not loud and in_loud:
            silence_start_frame = i
            in_loud = False
            # check if silence is long enough to be a real gap
            # (handled by ignoring short gaps below)
        # flush end
    if in_loud:
        # final loud region
        pass

    # Re-walk: build "kept" = list of [start, end] where the gap between
    # adjacent loud regions < min_silence_frames is merged.
    loud_starts = []
    loud_ends = []
    in_loud = False
    for i, loud in enumerate(is_loud):
        if loud and not in_loud:
            loud_starts.append(i)
            in_loud = True
        elif not loud and in_loud:
            loud_ends.append(i - 1)
            in_loud = False
    if in_loud:
        loud_ends.append(len(is_loud) - 1)

    # Merge adjacent loud regions whose gap < min_silence_frames
    merged = []
    for i, (s, e) in enumerate(zip(loud_starts, loud_ends)):
        if merged and s - merged[-1][1] < min_silence_frames:
            merged[-1] = (merged[-1][0], e)
        else:
            merged.append((s, e))

    kept_segments = [(s / frames_per_sec, (e + 1) / frames_per_sec)
                     for s, e in merged]

    if not kept_segments:
        log.warning("librosa: no loud regions detected — copying source as-is")
        shutil.copy(src, dst)
        return dst

    # Build concat filter for ffmpeg
    # Use select with "between(t,a,b)" on the source video + aselect on audio
    time_expr = "+".join(f"between(t,{a:.3f},{b:.3f})" for a, b in kept_segments)
    run([
        "ffmpeg", "-y", "-i", src,
        "-vf", f"select='{time_expr}',setpts=N/FRAME_RATE/TB",
        "-af", f"aselect='{time_expr}',asetpts=N/SR/TB",
        "-c:v", "libx264", "-preset", "ultrafast", "-pix_fmt", "yuv420p",
        "-c:a", "aac", "-b:a", "192k",
        dst,
    ])
    return dst


def remove_silence(src: str, dst: str,
                   threshold_percent: int = 4,
                   frame_margin_sec: float = 0.2,
                   engine: str = "auto-editor") -> str:
    """Pick engine. 'auto-editor' is default; 'librosa' is fallback."""
    if engine == "auto-editor":
        if shutil.which("auto-editor"):
            return remove_silence_auto_editor(src, dst, threshold_percent, frame_margin_sec)
        log.warning("auto-editor binary not found — falling back to librosa")
    return remove_silence_librosa(src, dst)


# ---------------------------------------------------------------------------
# 2. Viral candidate detection
# ---------------------------------------------------------------------------
def _score_segment(text: str, words_count: int, duration_sec: float,
                  has_keywords_list: List[str]) -> Dict[str, Any]:
    """Score a candidate segment. Higher score = more likely to be viral."""
    text_lower = text.lower()
    matched_kw = [kw for kw in has_keywords_list if kw in text_lower]
    word_density = words_count / max(duration_sec, 0.1)  # words per sec

    score = 0.0
    reasons: List[str] = []

    # Hook keyword presence (Hormozi "millions", "secret", etc.)
    kw_score = len(matched_kw) * 2.0
    score += kw_score
    if matched_kw:
        reasons.append(f"keywords({len(matched_kw)}): {','.join(matched_kw[:5])}")

    # Word density (high = "tight, fast" delivery)
    if word_density >= 3.5:
        score += 3.0
        reasons.append(f"high_density={word_density:.2f}")
    elif word_density >= 2.5:
        score += 1.5
        reasons.append(f"medium_density={word_density:.2f}")

    # Length sweet spot: 25-75s
    if 25 <= duration_sec <= 75:
        score += 2.0
        reasons.append(f"sweet_spot_duration={duration_sec:.1f}s")
    elif 15 <= duration_sec < 25:
        score += 1.0
        reasons.append(f"short_duration={duration_sec:.1f}s")
    elif 75 < duration_sec <= 120:
        score += 0.5
        reasons.append(f"long_duration={duration_sec:.1f}s")

    # Sentence starter hooks
    hook_starters = ["the first", "i will", "you need", "you should",
                     "you can't", "stop doing", "if you", "the truth",
                     "what if", "here's why", "this is"]
    if any(text_lower.startswith(h) for h in hook_starters):
        score += 1.5
        reasons.append("hook_starter")

    # Numbers present
    if re.search(r"\d", text):
        score += 1.0
        reasons.append("numbers_present")

    return {"score": round(score, 2), "reasons": reasons,
            "matched_keywords": matched_kw,
            "word_density": round(word_density, 2)}


def detect_viral_candidates(transcript_path: str,
                            target_duration_min: float = 25.0,
                            target_duration_max: float = 75.0,
                            keywords: Optional[List[str]] = None,
                            min_score: float = 3.0,
                            max_gap_sec: float = 0.5) -> List[Dict[str, Any]]:
    """
    Walk through transcript segments and produce candidate clips of length
    target_duration_min..max by merging consecutive segments.

    Each candidate has: start, end, duration_sec, text, words_count,
    score, reasons, hook_text (first 80 chars), start_word, end_word.
    """
    transcript = read_json(transcript_path)
    # Accept either full words.json (with "segments") or segments.json
    if "segments" in transcript:
        segs = transcript["segments"]
    elif isinstance(transcript, list):
        segs = transcript
    else:
        raise SystemExit(f"Unknown transcript format: {transcript_path}")

    if not segs:
        log.warning("No segments in transcript — cannot detect candidates")
        return []

    kw_list = keywords or HOOK_KEYWORDS

    # Strategy: greedy sliding window.
    # Pick a starting segment, then add consecutive segments until total
    # duration >= target_duration_min. Stop when reaching target_duration_max
    # OR score is high enough already.
    candidates: List[Dict[str, Any]] = []

    n = len(segs)
    for i in range(n):
        # accumulate consecutive segments
        start_t = segs[i]["start"]
        text_parts: List[str] = []
        words_count = 0
        last_end = start_t
        for j in range(i, min(i + 20, n)):  # max 20 segments forward
            s = segs[j]
            # check gap between consecutive segments
            if j > i and s["start"] - last_end > max_gap_sec:
                break  # gap too large — break the window
            text_parts.append(s["text"])
            words_count += len(s.get("words") or [s["text"]])
            last_end = s["end"]
            duration = last_end - start_t
            if duration >= target_duration_min:
                # candidate
                full_text = " ".join(text_parts).strip()
                score_data = _score_segment(full_text, words_count, duration, kw_list)
                if score_data["score"] >= min_score:
                    candidates.append({
                        "start": round(start_t, 3),
                        "end":   round(last_end, 3),
                        "duration_sec": round(duration, 3),
                        "text":  full_text,
                        "hook_text": full_text[:80],
                        "words_count": words_count,
                        "score": score_data["score"],
                        "reasons": score_data["reasons"],
                        "matched_keywords": score_data["matched_keywords"],
                        "word_density": score_data["word_density"],
                        "source_segment_start": i,
                        "source_segment_end": j,
                    })
                # if duration already >= target_duration_max, break to extend start
                if duration >= target_duration_max:
                    break

    # Deduplicate overlapping candidates: keep highest-scoring
    candidates.sort(key=lambda c: -c["score"])
    kept: List[Dict[str, Any]] = []
    for c in candidates:
        overlaps = False
        for k in kept:
            # overlap if they share >50% of either duration
            overlap_start = max(c["start"], k["start"])
            overlap_end = min(c["end"], k["end"])
            if overlap_end > overlap_start:
                overlap_dur = overlap_end - overlap_start
                if overlap_dur / c["duration_sec"] > 0.5 or \
                   overlap_dur / k["duration_sec"] > 0.5:
                    overlaps = True
                    break
        if not overlaps:
            kept.append(c)

    return kept


# ---------------------------------------------------------------------------
# 3. Cut clips out of source
# ---------------------------------------------------------------------------
def cut_clip(src: str, start: float, end: float, out_path: str,
             vertical: bool = True) -> str:
    """Cut [start,end] from src and re-encode."""
    Path(out_path).parent.mkdir(parents=True, exist_ok=True)
    vf = ["scale=1080:1920:force_original_aspect_ratio=increase",
          "crop=1080:1920"] if vertical else []
    cmd = [
        "ffmpeg", "-y", "-ss", f"{start:.3f}", "-to", f"{end:.3f}",
        "-i", src,
    ]
    if vf:
        cmd += ["-vf", ",".join(vf)]
    cmd += [
        "-c:v", "libx264", "-preset", "fast", "-crf", "20",
        "-pix_fmt", "yuv420p",
        "-c:a", "aac", "-b:a", "192k",
        "-avoid_negative_ts", "0",
        out_path,
    ]
    run(cmd)
    return out_path


# ---------------------------------------------------------------------------
# 4. Full auto-edit pipeline
# ---------------------------------------------------------------------------
def auto_edit(input_video: str,
              transcript_path: Optional[str] = None,
              out_dir: str = "auto_out",
              top_k: int = 5,
              min_score: float = 3.0,
              target_duration_min: float = 25.0,
              target_duration_max: float = 75.0,
              silence_threshold_percent: int = 4,
              silence_engine: str = "auto-editor",
              vertical: bool = True) -> Dict[str, Any]:
    """Run full auto-edit pipeline. Returns result dict."""
    out_dir_p = Path(out_dir)
    out_dir_p.mkdir(parents=True, exist_ok=True)

    base = Path(input_video).stem
    # Step 1: silence removal
    tight_path = out_dir_p / f"{base}.tight.mp4"
    log.info(f"[1/3] Removing silence from {input_video}")
    remove_silence(input_video, str(tight_path),
                   threshold_percent=silence_threshold_percent,
                   engine=silence_engine)
    tight_duration = probe_duration(str(tight_path))
    log.info(f"   silence-stripped duration: {tight_duration:.2f}s")

    # Step 2: detect candidates (on the ORIGINAL transcript — we don't
    # transcribe the tight version because we want the candidate ranges to
    # be on the original file's timeline. The tight version is just for
    # the final cut assembly.)
    if not transcript_path:
        # auto-transcribe the source
        from transcribe import transcribe  # type: ignore
        log.info(f"[2/3] Auto-transcribing source (no transcript provided)")
        td = transcribe(input_video, model_size="small")
        transcript_path = str(out_dir_p / f"{base}.words.json")
        write_json(td, transcript_path)
        transcript_data = td
    else:
        log.info(f"[2/3] Loading transcript: {transcript_path}")
        transcript_data = read_json(transcript_path)

    candidates = detect_viral_candidates(
        transcript_path,
        target_duration_min=target_duration_min,
        target_duration_max=target_duration_max,
        min_score=min_score,
    )
    log.info(f"   {len(candidates)} candidates detected (after dedup)")

    # Step 3: cut top-K clips
    log.info(f"[3/3] Cutting top-{top_k} clips")
    cuts_dir = out_dir_p / f"{base}.cuts"
    cuts_dir.mkdir(parents=True, exist_ok=True)
    cuts: List[Dict[str, Any]] = []
    for i, c in enumerate(candidates[:top_k]):
        clip_path = cuts_dir / f"cut_{i:02d}_{int(c['start'])}-{int(c['end'])}.mp4"
        # Cut from the SOURCE (full file), so the clip includes original
        # audio + visual context.
        cut_clip(input_video, c["start"], c["end"], str(clip_path), vertical=vertical)
        c["file"] = str(clip_path)
        c["index"] = i
        cuts.append(c)
        log.info(f"   cut_{i:02d}: {c['duration_sec']:.1f}s score={c['score']:.2f} "
                 f"hook='{c['hook_text'][:50]}'")

    # Save candidates manifest
    manifest_path = out_dir_p / f"{base}.candidates.json"
    write_json({
        "input": input_video,
        "transcript": transcript_path,
        "tightened_file": str(tight_path),
        "tight_duration_sec": tight_duration,
        "source_duration_sec": probe_duration(input_video),
        "language": transcript_data.get("language"),
        "candidates_all": candidates,
        "top_cuts": cuts,
        "params": {
            "min_score": min_score,
            "target_duration_min": target_duration_min,
            "target_duration_max": target_duration_max,
            "silence_threshold_percent": silence_threshold_percent,
            "silence_engine": silence_engine,
            "top_k": top_k,
        },
    }, manifest_path)
    return {
        "tightened_file": str(tight_path),
        "candidates_manifest": str(manifest_path),
        "cuts": cuts,
        "n_candidates": len(candidates),
    }


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------
def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("input", help="Source video file path")
    ap.add_argument("--transcript", default=None,
                    help="Pre-existing transcript .words.json (skip auto-transcribe)")
    ap.add_argument("--out-dir", default="auto_out",
                    help="Output directory for tight.mp4 + cuts/ + manifest.json")
    ap.add_argument("--top-k", type=int, default=5,
                    help="Number of top candidates to actually cut (default 5)")
    ap.add_argument("--min-score", type=float, default=3.0,
                    help="Minimum score threshold for candidate (default 3.0)")
    ap.add_argument("--min-dur", type=float, default=25.0,
                    help="Min candidate duration sec (default 25)")
    ap.add_argument("--max-dur", type=float, default=75.0,
                    help="Max candidate duration sec (default 75)")
    ap.add_argument("--silence-threshold", type=int, default=4,
                    help="auto-editor silence threshold percent (default 4)")
    ap.add_argument("--silence-engine", default="auto-editor",
                    choices=["auto-editor", "librosa"])
    ap.add_argument("--no-vertical", action="store_true",
                    help="Do not force 9:16 vertical (keep source aspect)")
    ap.add_argument("--list-only", action="store_true",
                    help="List candidates without cutting files")
    args = ap.parse_args()

    if args.list_only and args.transcript:
        cands = detect_viral_candidates(args.transcript,
                                       target_duration_min=args.min_dur,
                                       target_duration_max=args.max_dur,
                                       min_score=args.min_score)
        for i, c in enumerate(cands[:args.top_k * 3]):
            print(f"#{i:02d} score={c['score']:.2f} dur={c['duration_sec']:.1f}s "
                  f"start={c['start']:.1f} end={c['end']:.1f} "
                  f"reasons={','.join(c['reasons'][:3])}")
            print(f"    hook: {c['hook_text']}")
        return

    result = auto_edit(
        input_video=args.input,
        transcript_path=args.transcript,
        out_dir=args.out_dir,
        top_k=args.top_k,
        min_score=args.min_score,
        target_duration_min=args.min_dur,
        target_duration_max=args.max_dur,
        silence_threshold_percent=args.silence_threshold,
        silence_engine=args.silence_engine,
        vertical=not args.no_vertical,
    )
    print(json.dumps({
        "tightened_file": result["tightened_file"],
        "candidates_manifest": result["candidates_manifest"],
        "n_candidates": result["n_candidates"],
        "n_cuts": len(result["cuts"]),
        "cuts": [{"file": c["file"], "score": c["score"],
                  "duration_sec": c["duration_sec"],
                  "hook_text": c["hook_text"]} for c in result["cuts"]],
    }, indent=2))


if __name__ == "__main__":
    main()
