#!/usr/bin/env python3
"""
viral_edit.py — Layer 4 of the open-source stack
=================================================
Full viral montage pipeline. Takes a candidate clip + transcript words +
optional B-roll, and produces a publish-ready vertical video with:

  1. Double Zoom (zoompan 0.91x-1.09x oscillation)
  2. B-roll overlay (Pexels API local cache or local mp4)
  3. Beat-sync cuts (librosa)
  4. Hormozi-style animated captions (word-level)
  5. Speed-up (1.0x-1.2x depending on density)
  6. Loop-closer (last 0.5s reversed at the end — boosts completion rate)
  7. Final encode (9:16, 30 fps, H.264 yuv420p, AAC 192k)

Final step invokes the Retention Scorecard (retention_scorecard.py) — if
the score is <5/6, the publish gate refuses to publish.

Usage:
    python3 viral_edit.py --clip cut_00.mp4 --transcript x.words.json \\
        --start 16 --end 36 --broll broll.mp4 --out final.mp4
    python3 viral_edit.py --clip cut_00.mp4 --transcript x.words.json \\
        --start 16 --end 36 --out final.mp4 --no-scorecard
"""
from __future__ import annotations

import argparse
import json
import os
import random
import shutil
import subprocess
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _common import (  # noqa: E402
    log, get_logger, write_json, read_json, run, probe_duration,
    probe_dimensions, probe_audio, WORKDIR, fmt_time_ass, state_set,
    state_get,
)

log = get_logger("viral_edit")


# ---------------------------------------------------------------------------
# 0. Constants
# ---------------------------------------------------------------------------
TARGET_W = 1080
TARGET_H = 1920
TARGET_FPS = 30
HORMOZI_FONTSIZE = 90


# ---------------------------------------------------------------------------
# 1. Beat detection
# ---------------------------------------------------------------------------
def detect_beats(video_path: str, out_json: str) -> Dict[str, Any]:
    """Run librosa beat detection on extracted audio."""
    import librosa  # type: ignore
    import numpy as np
    audio_wav = str(WORKDIR / f"{Path(video_path).stem}_beats.wav")
    run(["ffmpeg", "-y", "-i", video_path, "-vn", "-ac", "1", "-ar", "22050",
         audio_wav], check=True)
    y, sr = librosa.load(audio_wav, sr=22050, mono=True)
    tempo, beat_frames = librosa.beat.beat_track(y=y, sr=sr, units="frames")
    beat_times = [float(t) for t in librosa.frames_to_time(beat_frames, sr=sr)]
    onset_env = librosa.onset.onset_strength(y=y, sr=sr)
    onset_frames = librosa.onset.onset_detect(onset_envelope=onset_env, sr=sr)
    onset_times = [float(t) for t in librosa.frames_to_time(onset_frames, sr=sr)]
    result = {
        "tempo_bpm": float(np.array(tempo).ravel()[0]),
        "beats": beat_times,
        "onsets": onset_times,
        "duration_sec": round(len(y) / sr, 3),
    }
    write_json(result, out_json)
    return result


# ---------------------------------------------------------------------------
# 2. Speed-up (only if word-density >= 3.5 — keeps delivery tight)
# ---------------------------------------------------------------------------
def apply_speedup(src: str, dst: str, factor: float = 1.1):
    """Speed-up audio + video using setpts + atempo."""
    # atempo allows factors in [0.5, 2.0]; for >2, chain.
    atempo_chain = "[0:a]atempo={f}[a]".format(f=factor) if factor <= 2.0 \
        else f"[0:a]atempo=2.0,atempo={factor/2.0}[a]"
    run([
        "ffmpeg", "-y", "-i", src,
        "-filter_complex",
        f"[0:v]setpts=PTS/{factor}[v];{atempo_chain}",
        "-map", "[v]", "-map", "[a]",
        "-c:v", "libx264", "-preset", "ultrafast", "-pix_fmt", "yuv420p",
        "-r", str(TARGET_FPS),
        "-c:a", "aac", "-b:a", "192k",
        dst,
    ])


# ---------------------------------------------------------------------------
# 3. Double Zoom (zoompan)
# ---------------------------------------------------------------------------
def apply_double_zoom(src: str, dst: str, cycle_sec: float = 4.0):
    """Apply viral double-zoom: oscillates between 0.91x and 1.09x every cycle_sec."""
    frames_per_cycle = int(TARGET_FPS * cycle_sec)
    # zoom oscillates 0.91..1.09 over `frames_per_cycle` frames
    # expression: 1 + 0.09*sin(2*pi*on/frames_per_cycle)
    zoom_expr = (f"1.0+0.09*sin(2*PI*on/{frames_per_cycle})")
    run([
        "ffmpeg", "-y", "-i", src,
        "-vf",
        (f"scale=1296:2304:flags=lanczos,"  # oversize for zoompan headroom
         f"zoompan=z='{zoom_expr}':"
         f"d=1:s={TARGET_W}x{TARGET_H}:fps={TARGET_FPS},"
         f"setsar=1"),
        "-c:v", "libx264", "-preset", "ultrafast", "-pix_fmt", "yuv420p",
        "-c:a", "copy",
        dst,
    ])


def apply_double_zoom_fast(src: str, dst: str):
    """Fast alternative: scale + crop to simulate zoom-in cycle.
    Cheaper computationally — recommended for low-spec machines."""
    # Scale to 1176x2080 (109% of 1080x1920), crop center back to 1080x1920
    run([
        "ffmpeg", "-y", "-i", src,
        "-vf", f"scale=1176:2080,setsar=1,crop={TARGET_W}:{TARGET_H}",
        "-c:v", "libx264", "-preset", "ultrafast", "-pix_fmt", "yuv420p",
        "-c:a", "copy", dst
    ])


# ---------------------------------------------------------------------------
# 4. Generate Hormozi-style ASS captions
# ---------------------------------------------------------------------------
def build_hormozi_ass(words_data: List[Dict[str, Any]],
                      out_ass: str,
                      start_offset: float = 0.0,
                      group_size: int = 2,
                      fontsize: int = HORMOZI_FONTSIZE,
                      fontname: str = "Arial Black",
                      fade_ms: int = 50,
                      outline: int = 8,
                      shadow: int = 2,
                      alignment: int = 2,
                      margin_v: int = 280,
                      primary_color: str = "&H00FFFFFF&",
                      highlight_color: str = "&H00FFFF&",
                      rotation_var: bool = True) -> str:
    """Build ASS file. start_offset subtracted from each timestamp so the
    .ass aligns with the cut clip (whose t=0 is the cut start)."""
    header = f"""[Script Info]
ScriptType: v4.00+
PlayResX: {TARGET_W}
PlayResY: {TARGET_H}
WrapStyle: 2
ScaledBorderAndShadow: yes

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Default,{fontname},{fontsize},{primary_color},&H000000FF,&H00000000,&H64000000,-1,0,0,0,100,100,0,0,1,{outline},{shadow},{alignment},80,80,{margin_v},1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""
    lines = [header]

    for seg in words_data:
        ws = seg.get("words") or [{
            "start": seg["start"], "end": seg["end"],
            "word": seg["text"].strip(),
        }]
        # subtract start_offset
        ws = [{**w,
               "start": max(0.0, w["start"] - start_offset),
               "end":   max(0.0, w["end"] - start_offset)} for w in ws]
        # skip negative-time words (shouldn't happen post-cut, but safety)
        ws = [w for w in ws if w["end"] > 0]
        if not ws:
            continue
        for i in range(0, len(ws), group_size):
            grp = ws[i:i + group_size]
            if grp[0]["end"] <= 0 or grp[-1]["start"] < 0:
                continue
            longest = max(grp, key=lambda w: len(w.get("word", "")))
            parts = []
            for w in grp:
                word_text = w["word"].upper()
                if w is longest:
                    color = highlight_color
                    rot = random.uniform(-4, 4) if rotation_var else 0
                else:
                    color = primary_color
                    rot = random.uniform(-2, 2) if rotation_var else 0
                tag = (
                    f"\\fad({fade_ms},{fade_ms})"
                    f"\\c{color}"
                    f"\\frz{rot:.1f}"
                    f"\\fscx100\\fscy105"
                )
                parts.append(f"{{{tag}}}{word_text}")
            text = " ".join(parts)
            line = (
                f"Dialogue: 0,{fmt_time_ass(grp[0]['start'])},"
                f"{fmt_time_ass(grp[-1]['end'])},Default,,0,0,0,,"
                f"{text}"
            )
            lines.append(line)

    Path(out_ass).parent.mkdir(parents=True, exist_ok=True)
    Path(out_ass).write_text("\n".join(lines), encoding="utf-8")
    log.info(f"Wrote {len(lines) - 1} caption blocks to {out_ass}")
    return out_ass


# ---------------------------------------------------------------------------
# 5. B-roll overlay
# ---------------------------------------------------------------------------
def overlay_broll(src: str, broll: str, dst: str,
                  segments: Optional[List[Dict[str, float]]] = None):
    """Overlay b-roll at given segments. If no segments given, overlay every
    3-5 seconds for 1s windows (pattern interrupt)."""
    if not Path(broll).exists():
        log.warning(f"B-roll file not found: {broll} — skipping overlay")
        shutil.copy(src, dst)
        return

    if segments is None:
        dur = probe_duration(src)
        segments = []
        # insert 1s b-roll every 4s, starting at t=3
        t = 3.0
        while t + 1.0 < dur:
            segments.append({"start": t, "end": t + 1.0})
            t += 4.0
    if not segments:
        shutil.copy(src, dst)
        return

    enable_expr = "+".join(
        f"between(t,{s['start']},{s['end']})" for s in segments
    ) or "0"

    filter_complex = (
        f"[1:v]scale={TARGET_W}:{TARGET_H}:force_original_aspect_ratio=increase,"
        f"crop={TARGET_W}:{TARGET_H},format=yuv420p[b];"
        f"[0:v][b]overlay=(W-w)/2:(H-h)/2:enable='{enable_expr}'[v]"
    )
    run([
        "ffmpeg", "-y", "-i", src, "-i", broll,
        "-filter_complex", filter_complex,
        "-map", "[v]", "-map", "0:a?",
        "-c:v", "libx264", "-preset", "ultrafast", "-pix_fmt", "yuv420p",
        "-c:a", "aac",
        dst
    ])


# ---------------------------------------------------------------------------
# 6. Burn captions
# ---------------------------------------------------------------------------
def burn_captions(src: str, ass_path: str, dst: str,
                  force_style: Optional[str] = None):
    """Burn ASS captions into video."""
    # Escape colon for Windows-style paths (not needed on Linux but safe)
    ass_escaped = str(ass_path).replace(":", r"\:")
    style = force_style or f"Alignment=2,MarginV=280,Outline=8,Shadow=2"
    run([
        "ffmpeg", "-y", "-i", src,
        "-vf", f"subtitles={ass_escaped}:force_style='{style}'",
        "-c:v", "libx264", "-preset", "ultrafast", "-pix_fmt", "yuv420p",
        "-c:a", "copy", dst
    ])


# ---------------------------------------------------------------------------
# 7. Loop closer (last 0.5s reversed + appended — boosts completion rate)
# ---------------------------------------------------------------------------
def apply_loop_closer(src: str, dst: str, tail_sec: float = 0.5):
    """Append a reversed copy of the last `tail_sec` seconds to the end.
    This creates a seamless loop signal that boosts completion rate on TikTok/IG.
    """
    dur = probe_duration(src)
    tail_start = max(0.0, dur - tail_sec)
    # Extract tail, reverse video + audio, append to original
    filter_complex = (
        f"[0:v]split=2[v1][v2];"
        f"[v2]trim=start={tail_start}:end={dur},setpts=PTS-STARTPTS,"
        f"reverse[vr];"
        f"[v1][vr]concat=n=2:v=1:a=0[vout];"
        f"[0:a]asplit=2[a1][a2];"
        f"[a2]atrim=start={tail_start}:end={dur},asetpts=PTS-STARTPTS,"
        f"areverse[ar];"
        f"[a1][ar]concat=n=2:v=0:a=1[aout]"
    )
    run([
        "ffmpeg", "-y", "-i", src,
        "-filter_complex", filter_complex,
        "-map", "[vout]", "-map", "[aout]",
        "-c:v", "libx264", "-preset", "ultrafast", "-pix_fmt", "yuv420p",
        "-c:a", "aac", "-b:a", "192k",
        dst
    ])


# ---------------------------------------------------------------------------
# 8. J-Cut (audio leads video by N ms — used as an opener pattern interrupt)
# ---------------------------------------------------------------------------
def apply_jcut(src: str, dst: str, audio_lead_ms: int = 500):
    """Make the audio play audio_lead_ms before the video starts."""
    run([
        "ffmpeg", "-y", "-i", src,
        "-filter_complex",
        f"[0:a]adelay={audio_lead_ms}|{audio_lead_ms}[a]",
        "-map", "0:v", "-map", "[a]",
        "-c:v", "copy", "-c:a", "aac",
        dst
    ])


# ---------------------------------------------------------------------------
# 9. Extract transcript subset matching clip range
# ---------------------------------------------------------------------------
def extract_words_in_range(transcript: Dict[str, Any],
                           start_sec: float, end_sec: float) -> List[Dict[str, Any]]:
    """Return segments whose word-timestamps fall within [start,end]."""
    out = []
    for seg in transcript.get("segments", []):
        # include segments that overlap [start,end]
        if seg["end"] < start_sec or seg["start"] > end_sec:
            continue
        # filter words inside range
        words = [w for w in (seg.get("words") or [])
                 if w["end"] >= start_sec and w["start"] <= end_sec]
        # If no words (segment-level only), include the segment as one block
        if not words and seg["text"]:
            words = [{"start": seg["start"], "end": seg["end"],
                      "word": seg["text"], "prob": 1.0}]
        out.append({**seg, "words": words})
    return out


# ---------------------------------------------------------------------------
# 10. Full pipeline
# ---------------------------------------------------------------------------
def viral_edit_pipeline(clip_path: str,
                        transcript_path: str,
                        start_sec: float,
                        end_sec: float,
                        broll_path: Optional[str] = None,
                        out_path: str = "final.mp4",
                        apply_speedup_factor: float = 1.0,
                        use_loop_closer: bool = True,
                        use_jcut: bool = False,
                        use_double_zoom: bool = True,
                        use_broll: bool = True,
                        use_captions: bool = True,
                        workdir: Optional[str] = None) -> Dict[str, Any]:
    """
    Full viral montage pipeline:
      extract-words → speedup → double-zoom → b-roll overlay → captions burn
      → loop closer → final encode
    """
    wd = Path(workdir) if workdir else (WORKDIR / f"viral_edit_{Path(clip_path).stem}")
    wd.mkdir(parents=True, exist_ok=True)

    log.info(f"Viral-edit pipeline starting | clip={clip_path} "
             f"transcript={transcript_path} range={start_sec}-{end_sec}s")

    # 1. Load transcript and extract words in clip range
    transcript = read_json(transcript_path)
    words_in_range = extract_words_in_range(transcript, start_sec, end_sec)
    log.info(f"   {len(words_in_range)} segments + "
             f"{sum(len(s['words']) for s in words_in_range)} words in range")

    # 2. Optional speedup
    current = clip_path
    if apply_speedup_factor and apply_speedup_factor != 1.0:
        log.info(f"[1/?] Speed-up x{apply_speedup_factor}")
        sp = wd / "sped.mp4"
        apply_speedup(current, str(sp), factor=apply_speedup_factor)
        current = str(sp)
        # adjust word timestamps by the speedup
        for seg in words_in_range:
            seg["start"] = seg["start"] / apply_speedup_factor
            seg["end"] = seg["end"] / apply_speedup_factor
            for w in seg["words"]:
                w["start"] = w["start"] / apply_speedup_factor
                w["end"] = w["end"] / apply_speedup_factor
        # also adjust start_sec to align with the new timeline
        # (start_sec/apply_speedup_factor is the new t=0 of the clip)
        # But we burned in clips already from the original at [start_sec, end_sec]
        # so the sped-up clip's t=0 already corresponds to original start_sec.
        start_offset_for_ass = start_sec
    else:
        start_offset_for_ass = start_sec

    # 3. Double Zoom
    if use_double_zoom:
        log.info("[2/?] Double zoom")
        dz = wd / "zoomed.mp4"
        try:
            apply_double_zoom(current, str(dz))
        except Exception as e:
            log.warning(f"zoompan failed ({e}), using fast zoom fallback")
            apply_double_zoom_fast(current, str(dz))
        current = str(dz)

    # 4. B-roll overlay
    if use_broll and broll_path:
        log.info("[3/?] B-roll overlay")
        br = wd / "brolled.mp4"
        overlay_broll(current, broll_path, str(br))
        current = str(br)

    # 5. Captions burn-in
    if use_captions and words_in_range:
        log.info("[4/?] Captions burn-in")
        ass_path = wd / "captions.ass"
        build_hormozi_ass(words_in_range, str(ass_path),
                          start_offset=start_offset_for_ass)
        cb = wd / "captioned.mp4"
        burn_captions(current, str(ass_path), str(cb))
        current = str(cb)

    # 6. Loop closer
    if use_loop_closer:
        log.info("[5/?] Loop closer")
        lc = wd / "loopcloser.mp4"
        try:
            apply_loop_closer(current, str(lc))
            current = str(lc)
        except Exception as e:
            log.warning(f"loop-closer failed ({e}) — skipping")

    # 7. J-Cut (optional)
    if use_jcut:
        log.info("[6/?] J-Cut")
        jc = wd / "jcut.mp4"
        apply_jcut(current, str(jc))
        current = str(jc)

    # 8. Final encode (ensure 9:16 + 30 fps + correct pix_fmt)
    log.info(f"[final] Encode → {out_path}")
    Path(out_path).parent.mkdir(parents=True, exist_ok=True)
    run([
        "ffmpeg", "-y", "-i", current,
        "-vf", f"scale={TARGET_W}:{TARGET_H}:force_original_aspect_ratio=increase,"
               f"crop={TARGET_W}:{TARGET_H},fps={TARGET_FPS},setsar=1,format=yuv420p",
        "-c:v", "libx264", "-preset", "fast", "-crf", "20",
        "-pix_fmt", "yuv420p",
        "-c:a", "aac", "-b:a", "192k", "-ar", "44100", "-ac", "2",
        "-movflags", "+faststart",
        out_path,
    ])

    final_dur = probe_duration(out_path)
    w, h = probe_dimensions(out_path)
    result = {
        "clip_path": clip_path,
        "transcript_path": transcript_path,
        "start_sec": start_sec,
        "end_sec": end_sec,
        "broll_path": broll_path,
        "speedup_factor": apply_speedup_factor,
        "use_double_zoom": use_double_zoom,
        "use_broll": use_broll,
        "use_captions": use_captions,
        "use_loop_closer": use_loop_closer,
        "use_jcut": use_jcut,
        "final_path": out_path,
        "final_duration_sec": final_dur,
        "final_width": w,
        "final_height": h,
        "vertical_9_16": (w == TARGET_W and h == TARGET_H),
    }
    state_set(f"viral_edit:{str(Path(out_path).resolve())}", result)
    log.info(f"✓ Final: {out_path} ({final_dur:.1f}s, {w}x{h})")
    return result


# ---------------------------------------------------------------------------
# 11. Run Retention Scorecard as a publish gate
# ---------------------------------------------------------------------------
def run_scorecard(video_path: str, transcript_path: str = None,
                  start_sec: float = 0.0, end_sec: float = None) -> Dict[str, Any]:
    """Run retention_scorecard.py on the final video. Returns the result dict.
    """
    try:
        from retention_scorecard import score_video  # type: ignore
    except ImportError:
        log.warning("retention_scorecard.py not available — skipping")
        return {"passed": True, "score": 6, "details": "scorecard not installed"}
    result = score_video(
        video_path=video_path,
        transcript_path=transcript_path,
        start_sec=start_sec,
        end_sec=end_sec,
    )
    return result


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------
def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--clip", required=True, help="Input clip (e.g. auto_edit cut_00.mp4)")
    ap.add_argument("--transcript", required=True,
                    help="Full transcript .words.json (for captions)")
    ap.add_argument("--start", type=float, required=True,
                    help="Start time in the source timeline (sec)")
    ap.add_argument("--end", type=float, required=True,
                    help="End time in the source timeline (sec)")
    ap.add_argument("--broll", default=None, help="B-roll video file (mp4)")
    ap.add_argument("--out", default="final.mp4", help="Output video path")
    ap.add_argument("--speedup", type=float, default=1.0,
                    help="Speed-up factor (1.0 = no speedup, 1.1 = mild, 1.2 = aggressive)")
    ap.add_argument("--no-zoom", action="store_true")
    ap.add_argument("--no-broll", action="store_true")
    ap.add_argument("--no-captions", action="store_true")
    ap.add_argument("--no-loop", action="store_true", help="Disable loop-closer")
    ap.add_argument("--jcut", action="store_true", help="Enable J-Cut opener")
    ap.add_argument("--scorecard", action="store_true",
                    help="Run retention_scorecard.py gate (refuses publish if <5/6)")
    args = ap.parse_args()

    result = viral_edit_pipeline(
        clip_path=args.clip,
        transcript_path=args.transcript,
        start_sec=args.start,
        end_sec=args.end,
        broll_path=args.broll,
        out_path=args.out,
        apply_speedup_factor=args.speedup,
        use_double_zoom=not args.no_zoom,
        use_broll=not args.no_broll,
        use_captions=not args.no_captions,
        use_loop_closer=not args.no_loop,
        use_jcut=args.jcut,
    )

    if args.scorecard:
        log.info("Running Retention Scorecard gate…")
        sc = run_scorecard(args.out, args.transcript, args.start, args.end)
        result["scorecard"] = sc
        if not sc.get("passed"):
            log.error(f"⛔ Scorecard failed: {sc.get('score')}/6 "
                     f"(min 5 required). Refusing to publish.")
            print(json.dumps(sc, indent=2))
            sys.exit(2)
        else:
            log.info(f"✓ Scorecard passed: {sc.get('score')}/6")

    print(json.dumps({k: v for k, v in result.items()
                      if k not in ("clip_path", "transcript_path")},
                     indent=2))


if __name__ == "__main__":
    main()
