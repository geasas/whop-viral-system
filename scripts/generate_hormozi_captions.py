#!/usr/bin/env python3
"""
generate_hormozi_captions.py
============================
Generate Alex-Hormozi-style animated captions (.ass subtitle file)
from a WhisperX / faster-whisper JSON transcript.

Features:
  - Word-level timing (1-3 words per caption block)
  - Bold uppercase font (Arial Black or similar)
  - Big 80-100pt size, positioned at bottom third
  - Fast 50ms fade in/out (Fast Move Text = ~3 frames @ 30fps)
  - Yellow highlight word + white surrounding words (Hormozi signature)
  - Optional rotation per word for variation
  - Outline + shadow for readability on any background

Usage:
    python3 generate_hormozi_captions.py transcript.json captions.ass

Or via the pipeline:
    from viral_pipeline import build_ass; build_ass(segments, "captions.ass")
"""
import argparse, json, random, sys

# Big bouncy color palette (Alex Hormozi style)
COLORS = [
    "&H00FFFF&",   # yellow (primary highlight)
    "&H0000FF&",   # red
    "&H00FFFFFF&", # white
    "&H0000FF00&", # green
    "&H0000FFFF&", # cyan
    "&H00FF8000&", # orange
]

def fmt_time(t: float) -> str:
    """0:00:00.00 format (centiseconds) expected by ASS."""
    h = int(t // 3600)
    m = int((t % 3600) // 60)
    s = t % 60
    return f"{h:d}:{m:02d}:{s:05.2f}"


def build_hormozi_ass(segments, out_path,
                      fontsize=90,
                      fontname="Arial Black",
                      group_size=2,
                      fade_ms=50,
                      outline=8,
                      shadow=2,
                      alignment=2,
                      margin_v=280,
                      rotation_var=True,
                      primary_color="&H00FFFFFF&",
                      highlight_color="&H00FFFF&"):
    """Build a Hormozi-style animated .ass subtitle file."""
    header = f"""[Script Info]
ScriptType: v4.00+
PlayResX: 1080
PlayResY: 1920
WrapStyle: 2
ScaledBorderAndShadow: yes

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Default,{fontname},{fontsize},{primary_color},&H000000FF,&H00000000,&H64000000,-1,0,0,0,100,100,0,0,1,{outline},{shadow},{alignment},80,80,{margin_v},1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""
    lines = [header]

    for seg in segments:
        ws = seg.get("words") or [{
            "start": seg["start"], "end": seg["end"],
            "word": seg["text"].strip()
        }]
        for i in range(0, len(ws), group_size):
            grp = ws[i:i+group_size]
            # Highlight the longest word in the group (Hormozi style)
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
                    f"\\frz{rot:.1f}"   # slight rotation for kinetic feel
                    f"\\fscx100\\fscy105"  # tiny scale pop on highlight word
                )
                parts.append(f"{{{tag}}}{word_text}")
            text = " ".join(parts)
            line = (
                f"Dialogue: 0,{fmt_time(grp[0]['start'])},"
                f"{fmt_time(grp[-1]['end'])},Default,,0,0,0,,"
                f"{text}"
            )
            lines.append(line)

    with open(out_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print(f"Wrote {len(lines)-1} caption blocks to {out_path}")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("transcript_json", help="Whisper transcript JSON")
    ap.add_argument("out_ass", help="Output .ass subtitle file")
    ap.add_argument("--font-size", type=int, default=90)
    ap.add_argument("--font-name", default="Arial Black")
    ap.add_argument("--group-size", type=int, default=2,
                    help="Words per caption (1-3 for Hormozi style)")
    ap.add_argument("--fade-ms", type=int, default=50)
    ap.add_argument("--no-rotation", action="store_true")
    args = ap.parse_args()

    with open(args.transcript_json) as f:
        segments = json.load(f)
    build_hormozi_ass(segments, args.out_ass,
                      fontsize=args.font_size,
                      fontname=args.font_name,
                      group_size=args.group_size,
                      fade_ms=args.fade_ms,
                      rotation_var=not args.no_rotation)


if __name__ == "__main__":
    main()
