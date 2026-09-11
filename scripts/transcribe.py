#!/usr/bin/env python3
"""
transcribe.py — Layer 2 of the open-source stack
================================================
Transcribe audio/video with faster-whisper.

Outputs:
  - <base>.srt            — SubRip subtitles (segment-level).
  - <base>.words.json      — Word-level timestamps (machine-readable).
  - <base>.segments.json   — Segment-level (machine-readable).
  - <base>.txt            — Plain-text transcript.

Features:
  - Automatic language detection (overridable with --language).
  - Word-level timestamps (required for Hormozi-style captions).
  - VAD filter (silence/long pauses stripped before ASR — improves accuracy).
  - GPU support via --device cuda (auto-detected).
  - State-tracked: re-running same file reuses cached transcript.

faster-whisper: https://github.com/SYSTRAN/faster-whisper (MIT).
Model sizes:    tiny, base, small, medium, large-v3, large-v3-pc.
                (small = recommended default; medium = best for AR; large-v3 for high-acc.)

Usage:
    python3 transcribe.py input.mp4 --model small --language en
    python3 transcribe.py input.mp4 --out-dir transcripts/
    python3 transcribe.py input.mp4 --device cuda     # GPU if available
"""
from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _common import (  # noqa: E402
    log, get_logger, write_json, read_json, state_set, state_get,
    fmt_time_srt, run, probe_duration, probe_audio,
)

log = get_logger("transcribe")


# ---------------------------------------------------------------------------
# GPU detection
# ---------------------------------------------------------------------------
def detect_device(prefer: str = "auto") -> str:
    """Return 'cuda' if GPU + CUDA available, else 'cpu'."""
    if prefer == "cpu":
        return "cpu"
    if prefer == "cuda":
        try:
            import torch  # type: ignore
            if torch.cuda.is_available():
                log.info(f"CUDA available: {torch.cuda.get_device_name(0)}")
                return "cuda"
        except ImportError:
            log.warning("PyTorch not installed — GPU acceleration disabled.")
        return "cpu"
    # auto
    try:
        import torch  # type: ignore
        if torch.cuda.is_available():
            log.info(f"Auto-detected CUDA: {torch.cuda.get_device_name(0)}")
            return "cuda"
    except ImportError:
        pass
    return "cpu"


# ---------------------------------------------------------------------------
# Transcription
# ---------------------------------------------------------------------------
def transcribe(file_path: str,
               model_size: str = "small",
               language: Optional[str] = None,
               device: str = "auto",
               compute_type: Optional[str] = None,
               vad_filter: bool = True,
               beam_size: int = 5,
               word_timestamps: bool = True) -> Dict[str, Any]:
    """
    Transcribe `file_path` with faster-whisper.

    Returns:
        {
          "language": "en", "language_probability": 0.99,
          "duration_sec": 8.0,
          "segments": [{start,end,text,words:[{start,end,word,prob}]}],
          "text": "full text"
        }
    """
    from faster_whisper import WhisperModel  # type: ignore

    dev = detect_device(device)
    if compute_type is None:
        compute_type = "float16" if dev == "cuda" else "int8"
    log.info(f"Loading WhisperModel '{model_size}' on {dev}/{compute_type}")
    model = WhisperModel(model_size, device=dev, compute_type=compute_type)

    # First extract audio if file is a video (faster-whisper accepts video,
    # but a 16 kHz mono wav is faster + more reliable).
    audio_path = file_path
    temp_audio = None
    if probe_audio(file_path):
        # Whisper handles audio in any format; pass directly.
        pass

    log.info(f"Transcribing {file_path}")
    seg_iter, info = model.transcribe(
        audio_path,
        language=language,
        beam_size=beam_size,
        word_timestamps=word_timestamps,
        vad_filter=vad_filter,
        vad_parameters=dict(min_silence_duration_ms=500) if vad_filter else None,
    )
    segments: List[Dict[str, Any]] = []
    full_text_parts: List[str] = []
    for seg in seg_iter:
        words = []
        if seg.words:
            for w in seg.words:
                words.append({
                    "start": round(float(w.start), 3),
                    "end":   round(float(w.end), 3),
                    "word":  w.word.strip(),
                    "prob":  round(float(w.probability), 3),
                })
        segments.append({
            "start": round(float(seg.start), 3),
            "end":   round(float(seg.end), 3),
            "text":  seg.text.strip(),
            "words": words,
        })
        full_text_parts.append(seg.text.strip())

    return {
        "language": info.language,
        "language_probability": round(float(info.language_probability), 4),
        "duration_sec": round(float(info.duration), 3),
        "duration_all_segments": round(
            segments[-1]["end"] if segments else 0.0, 3),
        "segments": segments,
        "text": " ".join(full_text_parts).strip(),
        "model": model_size,
        "device": dev,
        "vad_filter": vad_filter,
    }


# ---------------------------------------------------------------------------
# SRT writer
# ---------------------------------------------------------------------------
def write_srt(segments: List[Dict[str, Any]], out_path: str | Path) -> str:
    """Write SubRip (.srt) file from segment-level timestamps."""
    out = Path(out_path)
    out.parent.mkdir(parents=True, exist_ok=True)
    lines = []
    for i, s in enumerate(segments, 1):
        lines.append(str(i))
        lines.append(f"{fmt_time_srt(s['start'])} --> {fmt_time_srt(s['end'])}")
        lines.append(s["text"])
        lines.append("")
    out.write_text("\n".join(lines), encoding="utf-8")
    return str(out)


# ---------------------------------------------------------------------------
# Cache layer (state-tracked)
# ---------------------------------------------------------------------------
def get_cached(file_path: str, model_size: str) -> Optional[Dict[str, Any]]:
    """Return cached transcript if file modified before last transcription."""
    key = f"transcribe:{Path(file_path).resolve()}:{model_size}"
    cached = state_get(key)
    if not cached:
        return None
    if not Path(file_path).exists():
        return None
    if Path(file_path).stat().st_mtime > cached.get("source_mtime", 0):
        log.info("Source file modified — re-transcribing")
        return None
    return cached


def save_cache(file_path: str, model_size: str, data: Dict[str, Any]) -> None:
    data_with_meta = {**data,
                      "source_mtime": Path(file_path).stat().st_mtime,
                      "source_path": str(Path(file_path).resolve())}
    key = f"transcribe:{Path(file_path).resolve()}:{model_size}"
    state_set(key, data_with_meta)


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------
def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("input", help="Audio or video file path")
    ap.add_argument("--model", default="small",
                    choices=["tiny", "base", "small", "medium", "large-v3", "large-v3-pc"])
    ap.add_argument("--language", default=None,
                    help="Override language detection (e.g. en, ar)")
    ap.add_argument("--device", default="auto", choices=["auto", "cpu", "cuda"])
    ap.add_argument("--compute-type", default=None,
                    help="Override compute type (e.g. int8, float16)")
    ap.add_argument("--no-vad", action="store_true", help="Disable VAD filter")
    ap.add_argument("--beam-size", type=int, default=5)
    ap.add_argument("--no-words", action="store_true",
                    help="Skip word-level timestamps (faster, no word JSON)")
    ap.add_argument("--out-dir", default=None,
                    help="Output dir (default: same as input)")
    ap.add_argument("--out-base", default=None,
                    help="Base name (default: input file stem)")
    ap.add_argument("--force", action="store_true", help="Ignore cache")
    args = ap.parse_args()

    src = Path(args.input).resolve()
    if not src.exists():
        raise SystemExit(f"Input file not found: {src}")
    out_dir = Path(args.out_dir) if args.out_dir else src.parent
    out_dir.mkdir(parents=True, exist_ok=True)
    base = args.out_base or src.stem
    srt_path = out_dir / f"{base}.srt"
    words_path = out_dir / f"{base}.words.json"
    segs_path = out_dir / f"{base}.segments.json"
    txt_path = out_dir / f"{base}.txt"

    # Check cache
    if not args.force:
        cached = get_cached(str(src), args.model)
        if cached:
            log.info("Using cached transcript")
            # Re-write outputs from cache
            write_srt(cached["segments"], srt_path)
            write_json(cached, words_path)
            write_json({"segments": cached["segments"],
                        "language": cached["language"],
                        "duration_sec": cached["duration_sec"]},
                       segs_path)
            txt_path.write_text(cached["text"], encoding="utf-8")
            log.info(f"Wrote: {srt_path}, {words_path}, {segs_path}, {txt_path}")
            print(json.dumps({
                "language": cached["language"],
                "language_probability": cached["language_probability"],
                "duration_sec": cached["duration_sec"],
                "segments": len(cached["segments"]),
                "srt_path": str(srt_path),
                "words_path": str(words_path),
                "segments_path": str(segs_path),
                "txt_path": str(txt_path),
                "cached": True,
            }, indent=2))
            return

    # Run transcription
    data = transcribe(
        file_path=str(src),
        model_size=args.model,
        language=args.language,
        device=args.device,
        compute_type=args.compute_type,
        vad_filter=not args.no_vad,
        beam_size=args.beam_size,
        word_timestamps=not args.no_words,
    )

    # Write outputs
    write_srt(data["segments"], srt_path)
    write_json(data, words_path)  # full word-level
    write_json({"segments": data["segments"],
                "language": data["language"],
                "duration_sec": data["duration_sec"]},
               segs_path)
    txt_path.write_text(data["text"], encoding="utf-8")

    save_cache(str(src), args.model, data)
    log.info(f"Wrote: {srt_path}, {words_path}, {segs_path}, {txt_path}")
    print(json.dumps({
        "language": data["language"],
        "language_probability": data["language_probability"],
        "duration_sec": data["duration_sec"],
        "segments": len(data["segments"]),
        "words": sum(len(s["words"]) for s in data["segments"]),
        "srt_path": str(srt_path),
        "words_path": str(words_path),
        "segments_path": str(segs_path),
        "txt_path": str(txt_path),
    }, indent=2))


if __name__ == "__main__":
    main()
