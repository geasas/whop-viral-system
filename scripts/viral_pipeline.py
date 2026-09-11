#!/usr/bin/env python3
"""
Viral Short-Form Pipeline — Zero-Budget Open-Source Edition
==========================================================
End-to-end pipeline for Whop Content Rewards clipping:
  yt-dlp (download) → faster-whisper (transcribe w/ word timestamps)
  → auto-editor (silence/filler removal) → librosa (beat detection)
  → FFmpeg (B-roll + double-zoom + captions burn-in + J-Cut + closer)
  → final vertical short, ready to upload.

This is a runnable reference implementation. Sub-scripts can also run standalone.

Usage:
    python3 viral_pipeline.py --url "https://youtu.be/XXXX" --clip-start 60 --clip-end 90 \\
        --caption-color yellow --broll broll.mp4 --out final.mp4

Requirements (all free / open-source):
    pip install yt-dlp faster-whisper moviepy ffmpeg-python librosa soundfile numpy \\
                opencv-python-headless auto-editor
    apt install ffmpeg
"""

import argparse, json, os, subprocess, sys, shutil
from pathlib import Path
from typing import List, Dict, Optional

ROOT = Path(__file__).resolve().parent
WORKDIR = ROOT / "_pipeline_workdir"


# ---------------------------------------------------------------------------
# Helper — run command with live logging
# ---------------------------------------------------------------------------
def run(cmd: List[str], **kw):
    print(f"\n$ {' '.join(str(c) for c in cmd)}")
    return subprocess.run(cmd, check=True, **kw)


# ---------------------------------------------------------------------------
# 1. Download with yt-dlp
# ---------------------------------------------------------------------------
def download(url: str, out_tmpl: str = "%(id)s.%(ext)s", fmt: str = "bestvideo[height<=1080]+bestaudio/best[height<=1080]") -> str:
    """Download source video using yt-dlp. Returns path of downloaded file."""
    WORKDIR.mkdir(parents=True, exist_ok=True)
    out_path = WORKDIR / out_tmpl
    cmd = [
        "yt-dlp",
        "-f", fmt,
        "--merge-output-format", "mp4",
        "-o", str(out_path),
        "--no-playlist",
        "--write-auto-sub", "--sub-lang", "en,ar",
        "--convert-subs=srt",
        url,
    ]
    run(cmd)
    # Find the actual mp4 produced
    for p in WORKDIR.glob("*.mp4"):
        return str(p)
    raise RuntimeError("yt-dlp did not produce an mp4")


# ---------------------------------------------------------------------------
# 2. Extract a sub-clip (source can be long)
# ---------------------------------------------------------------------------
def extract_clip(src: str, start: float, end: float, out_path: str):
    """Lossless trim using FFmpeg's -ss/-to."""
    run([
        "ffmpeg", "-y", "-ss", str(start), "-to", str(end), "-i", src,
        "-c:v", "libx264", "-preset", "ultrafast", "-pix_fmt", "yuv420p",
        "-c:a", "aac", "-b:a", "192k",
        "-vf", "scale=-2:1920,crop=1080:1920",   # vertical 9:16
        out_path
    ])


# ---------------------------------------------------------------------------
# 3. Transcribe with faster-whisper (word-level timestamps)
# ---------------------------------------------------------------------------
def transcribe(audio_or_video: str, model_size: str = "small", language: str = None) -> List[Dict]:
    """Returns list of {start,end,text,words:[{start,end,word,prob}]}."""
    from faster_whisper import WhisperModel
    model = WhisperModel(model_size, device="cpu", compute_type="int8")
    seg_iter, info = model.transcribe(
        audio_or_video,
        language=language,
        word_timestamps=True,
        vad_filter=True,                 # removes long silences from ASR
        vad_parameters=dict(min_silence_duration_ms=500),
    )
    out = []
    for seg in seg_iter:
        seg_dict = {
            "start": round(seg.start, 3),
            "end":   round(seg.end, 3),
            "text":  seg.text.strip(),
            "words": [],
        }
        if seg.words:
            seg_dict["words"] = [
                {"start": round(w.start, 3), "end": round(w.end, 3),
                 "word": w.word.strip(), "prob": round(float(w.probability), 3)}
                for w in seg.words
            ]
        out.append(seg_dict)
    return out


# ---------------------------------------------------------------------------
# 4. Remove silence / fillers with auto-editor
# ---------------------------------------------------------------------------
def remove_silence(src: str, dst: str,
                   threshold_percent: int = 4,    # cut below 4% peak volume
                   frame_margin: int = 4):       # keep 4 frames around each kept region
    """Use auto-editor to cut silence and breath gaps."""
    cmd = [
        "auto-editor", src,
        "--edit", f"audio:{threshold_percent}%",
        "--margin", f"{frame_margin}f",
        "--when-silent", "cut",
        "--when-active", "nil",
        "-o", dst,
        "--no-open",                       # skip launching a viewer
        "--export", "default",
    ]
    run(cmd)


# ---------------------------------------------------------------------------
# 5. Beat detection with librosa (for Beat Sync cuts)
# ---------------------------------------------------------------------------
def detect_beats(audio_path: str, out_json: str = "beats.json") -> Dict:
    import librosa, numpy as np
    y, sr = librosa.load(audio_path, sr=22050, mono=True)
    tempo, beat_frames = librosa.beat.beat_track(y=y, sr=sr, units="frames")
    beat_times = [float(t) for t in librosa.frames_to_time(beat_frames, sr=sr)]
    # Also detect onset envelopes for finer cuts
    onset_env = librosa.onset.onset_strength(y=y, sr=sr)
    onset_frames = librosa.onset.onset_detect(onset_envelope=onset_env, sr=sr)
    onset_times = [float(t) for t in librosa.frames_to_time(onset_frames, sr=sr)]
    result = {
        "tempo_bpm": float(np.array(tempo).ravel()[0]),
        "beats": beat_times,
        "onsets": onset_times,
        "duration_sec": round(len(y) / sr, 3),
    }
    with open(out_json, "w") as f:
        json.dump(result, f, indent=2)
    return result


# ---------------------------------------------------------------------------
# 6. Generate Hormozi-style animated captions as ASS subtitle file
# ---------------------------------------------------------------------------
def build_ass(words_data: List[Dict], out_ass: str = "captions.ass",
              fontsize: int = 80, primary_color: str = "&H00FFFFFF",
              outline_color: str = "&H00000000"):
    """
    Build an ASS subtitle file with 1-3 word groups per dialogue line,
    fast fade in/out, Alex-Hormozi-style big bouncy text.
    """
    ass_header = f"""[Script Info]
ScriptType: v4.00+
PlayResX: 1080
PlayResY: 1920
WrapStyle: 2

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Default,Arial Black,{fontsize},{primary_color},&H000000FF,{outline_color},&H64000000,-1,0,0,0,100,100,0,0,1,8,2,2,80,80,360,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""
    lines = [ass_header]
    # Build word groups of size 2 (Hormozi-style: 1-3 words per caption)
    GROUP_SIZE = 2
    for seg in words_data:
        ws = seg.get("words") or []
        # If no word timestamps, use whole segment
        if not ws:
            ws = [{"start": seg["start"], "end": seg["end"], "word": seg["text"]}]
        for i in range(0, len(ws), GROUP_SIZE):
            grp = ws[i:i+GROUP_SIZE]
            text = " ".join(w["word"] for w in grp)
            # Add a slight rotation/color variety per word
            tag = "\\fad(50,50)\\c&H00FFFF&"  # fade + yellow
            line = (
                f"Dialogue: 0,{_fmt_time(grp[0]['start'])},"
                f"{_fmt_time(grp[-1]['end'])},Default,,0,0,0,,"
                f"{{{tag}}}{text}"
            )
            lines.append(line)
    with open(out_ass, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    return out_ass


def _fmt_time(t: float) -> str:
    """0:00:00.00 format expected by ASS."""
    h = int(t // 3600); m = int((t % 3600) // 60); s = t % 60
    return f"{h:d}:{m:02d}:{s:05.2f}"


# ---------------------------------------------------------------------------
# 7. Apply Double Zoom (91% ← 100% ← 109% over 4-5s cycles)
# ---------------------------------------------------------------------------
def apply_double_zoom(src: str, dst: str):
    """
    Apply the signature 'double zoom' used by viral editors.
    Uses zoompan with a saw-tooth oscillation between 0.91x and 1.09x every 4s.
    """
    zoom_expr = (
        # zoom oscillates 0.91 -> 1.0 -> 1.09 over each 4-second cycle
        "if(lte(on,1),1.0,0.91+0.18*abs(mod(on/((30*4)/2),2)-1))"
    )
    # The expression above cycles between 0.91 and 1.09 across 4s (30fps * 4s = 120 frames)
    # Simpler approach: use the zoompan sawtooth
    cmd = [
        "ffmpeg", "-y", "-i", src,
        "-vf", f"zoompan=z='0.91+0.18*abs(mod(on,120)/120.0-0.5)*2':"
               f"d=1:s=1080x1920:fps=30",
        "-c:v", "libx264", "-preset", "ultrafast", "-pix_fmt", "yuv420p",
        "-c:a", "copy",
        dst
    ]
    # NOTE: zoompan on 1080x1920 video may be slow; alternative = scale + crop
    run(cmd)


def apply_double_zoom_fast(src: str, dst: str):
    """
    Fast alternative: scale up + crop center to simulate zoom-in cycle.
    Cheaper computationally — recommended for low-spec machines.
    """
    # Scale to 1176x2080 (109% of 1080x1920), crop center back to 1080x1920
    run([
        "ffmpeg", "-y", "-i", src,
        "-vf", "scale=1176:2080,setsar=1,crop=1080:1920",
        "-c:v", "libx264", "-preset", "ultrafast", "-pix_fmt", "yuv420p",
        "-c:a", "copy", dst
    ])


# ---------------------------------------------------------------------------
# 8. B-roll overlay
# ---------------------------------------------------------------------------
def overlay_broll(src: str, broll: str, dst: str, segments: List[Dict]):
    """
    Overlay b-roll clips at given time segments.
    segments = [{"start": 2.0, "end": 5.0, "x": "center", "y": "center", "scale": 1.0}]
    """
    enable_expr = "+".join(
        f"between(t,{s['start']},{s['end']})" for s in segments
    ) or "0"
    # x,y = center of 1080x1920 frame
    # The broll is first scaled to fit the target dim
    filter_complex = (
        f"[1:v]scale=1080:1920:force_original_aspect_ratio=increase,"
        f"crop=1080:1920[b];"
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
# 9. J-Cut (audio leads video by N ms)
# ---------------------------------------------------------------------------
def apply_jcut(src: str, dst: str, audio_lead_ms: int = 500):
    """Make the audio play audio_lead_ms before the video starts."""
    run([
        "ffmpeg", "-y", "-i", src,
        "-filter_complex", f"[0:a]adelay={audio_lead_ms}|{audio_lead_ms}[a]",
        "-map", "0:v", "-map", "[a]",
        "-c:v", "copy", "-c:a", "aac",
        dst
    ])


# ---------------------------------------------------------------------------
# 10. Burn captions into video (Hormozi style)
# ---------------------------------------------------------------------------
def burn_captions(src: str, ass_path: str, dst: str):
    """Burn in the ASS captions."""
    # Important: escape the colon in the ass path (Windows) or use absolute path
    ass_escaped = ass_path.replace(":", r"\:")
    run([
        "ffmpeg", "-y", "-i", src,
        "-vf", f"subtitles={ass_escaped}:force_style='Alignment=2,MarginV=360'",
        "-c:v", "libx264", "-preset", "ultrafast", "-pix_fmt", "yuv420p",
        "-c:a", "copy", dst
    ])


# ---------------------------------------------------------------------------
# 11. Beat-sync cuts (using detected beats)
# ---------------------------------------------------------------------------
def beat_sync_cuts(src: str, beats_json: str, dst: str, min_clip: float = 0.5):
    """
    Cut the source at every detected beat, then re-concatenate.
    Produces a fast-paced, music-synced edit.
    """
    with open(beats_json) as f:
        beats = json.load(f)["beats"]
    beats = [0.0] + beats + [None]  # None = end-of-video; we'll use ffprobe to find duration
    # Get duration
    probe = subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration",
         "-of", "default=noprint_wrappers=1:nokey=1", src],
        capture_output=True, text=True
    )
    duration = float(probe.stdout.strip())
    beats[-1] = duration

    # Generate sub-segments list file
    concat_file = WORKDIR / "concat.txt"
    parts_dir = WORKDIR / "beat_parts"
    parts_dir.mkdir(exist_ok=True)
    with open(concat_file, "w") as f:
        for i, (b0, b1) in enumerate(zip(beats[:-1], beats[1:])):
            if b1 - b0 < min_clip:
                continue
            part = parts_dir / f"part_{i:04d}.mp4"
            run([
                "ffmpeg", "-y", "-ss", str(b0), "-to", str(b1), "-i", src,
                "-c:v", "libx264", "-preset", "ultrafast", "-pix_fmt", "yuv420p",
                "-c:a", "aac", "-avoid_negative_ts", "0",
                str(part)
            ])
            f.write(f"file '{part}'\n")
    # Concatenate
    run([
        "ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", str(concat_file),
        "-c", "copy", dst
    ])


# ---------------------------------------------------------------------------
# 12. Full pipeline (orchestration)
# ---------------------------------------------------------------------------
def pipeline(url: str, clip_start: float, clip_end: float,
             broll_path: Optional[str] = None,
             caption_color: str = "yellow",
             model_size: str = "small",
             out_path: str = "final.mp4"):
    """
    Full viral short-form pipeline:
        download → trim → transcribe → silence-removal → beat-sync → double-zoom
        → captions burn-in → b-roll overlay → J-Cut → final
    """
    WORKDIR.mkdir(parents=True, exist_ok=True)

    print("[1/9] Downloading source via yt-dlp…")
    src_path = download(url)

    print("[2/9] Extracting vertical sub-clip…")
    raw_clip = str(WORKDIR / "raw_clip.mp4")
    extract_clip(src_path, clip_start, clip_end, raw_clip)

    print("[3/9] Transcribing with faster-whisper (word-level)…")
    segments = transcribe(raw_clip, model_size=model_size)
    (WORKDIR / "transcript.json").write_text(json.dumps(segments, indent=2, ensure_ascii=False))

    print("[4/9] Removing silence/fillers with auto-editor…")
    tight_clip = str(WORKDIR / "tight.mp4")
    remove_silence(raw_clip, tight_clip, threshold_percent=4, frame_margin=4)

    print("[5/9] Detecting beats with librosa…")
    audio_only = str(WORKDIR / "audio.wav")
    run(["ffmpeg", "-y", "-i", tight_clip, "-vn", "-ac", "1", "-ar", "22050", audio_only])
    beats_data = detect_beats(audio_only, str(WORKDIR / "beats.json"))

    print("[6/9] Beat-sync cuts (optional — only if beats > 4)…")
    if len(beats_data["beats"]) >= 4:
        beat_synced = str(WORKDIR / "beat_synced.mp4")
        beat_sync_cuts(tight_clip, str(WORKDIR / "beats.json"), beat_synced)
    else:
        beat_synced = tight_clip   # skip if not enough beats

    print("[7/9] Applying Double Zoom…")
    zoomed = str(WORKDIR / "zoomed.mp4")
    apply_double_zoom_fast(beat_synced, zoomed)

    print("[8/9] Generating Hormozi-style captions ASS…")
    color_map = {
        "yellow": "&H00FFFF&", "white": "&H00FFFFFF&",
        "red": "&H0000FF&", "green": "&H0000FF00&",
        "blue": "&H00FF0000&"
    }
    ass_path = build_ass(segments, str(WORKDIR / "captions.ass"),
                         primary_color=color_map.get(caption_color, "&H00FFFFFF&"))

    print("[9/9] Burning captions + (optional) B-roll + J-Cut…")
    final = str(WORKDIR / "final_captions.mp4")
    burn_captions(zoomed, ass_path, final)

    if broll_path and os.path.exists(broll_path):
        brolled = str(WORKDIR / "final_broll.mp4")
        overlay_broll(final, broll_path, brolled,
                      [{"start": 2.0, "end": 5.0},
                       {"start": 8.0, "end": 11.0}])
        final = brolled

    # J-Cut is optional — only if hook audio exists separately. Skip by default.
    shutil.copy(final, out_path)
    print(f"\n✅ Done. Final video: {out_path}")
    print(f"   Workdir: {WORKDIR}")
    return out_path


# ---------------------------------------------------------------------------
# CLI entry
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    ap = argparse.ArgumentParser(description="Viral short-form pipeline (zero-budget).")
    ap.add_argument("--url",        required=True, help="Source URL (YouTube/etc)")
    ap.add_argument("--clip-start", type=float, default=0.0, help="Clip start seconds")
    ap.add_argument("--clip-end",   type=float, default=30.0, help="Clip end seconds")
    ap.add_argument("--broll",      default=None, help="Optional B-roll video path")
    ap.add_argument("--caption-color", default="yellow",
                    choices=["yellow", "white", "red", "green", "blue"])
    ap.add_argument("--model",      default="small", choices=["tiny", "base", "small", "medium", "large-v3"])
    ap.add_argument("--out",        default="final.mp4")
    args = ap.parse_args()

    pipeline(args.url, args.clip_start, args.clip_end,
             broll_path=args.broll, caption_color=args.caption_color,
             model_size=args.model, out_path=args.out)
