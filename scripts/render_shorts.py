#!/usr/bin/env python3
"""Render approved scripts into vertical MP4 Shorts. No copyrighted footage is downloaded."""
import asyncio
import json
import os
import re
import subprocess
import textwrap
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont
import edge_tts

ROOT = Path(__file__).resolve().parents[1]
QUEUE = ROOT / "content" / "queue.json"
OUT = ROOT / "output"
WIDTH, HEIGHT = 1080, 1920
FPS = 24


def font(size, bold=False):
    choices = [
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf" if bold else "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        "/usr/share/fonts/truetype/liberation2/LiberationSans-Bold.ttf" if bold else "/usr/share/fonts/truetype/liberation2/LiberationSans-Regular.ttf",
    ]
    for path in choices:
        if Path(path).exists():
            return ImageFont.truetype(path, size)
    return ImageFont.load_default()


def wrap_words(draw, text, fnt, max_width):
    words, lines, current = text.split(), [], ""
    for word in words:
        candidate = f"{current} {word}".strip()
        if draw.textbbox((0, 0), candidate, font=fnt)[2] <= max_width:
            current = candidate
        else:
            if current:
                lines.append(current)
            current = word
    if current:
        lines.append(current)
    return lines


def draw_card(text, label, out_path, index, total):
    image = Image.new("RGB", (WIDTH, HEIGHT), (13, 18, 35))
    draw = ImageDraw.Draw(image)
    # Simple original graphic treatment; no film stills or unlicensed footage.
    draw.rounded_rectangle((62, 90, WIDTH - 62, HEIGHT - 90), radius=42, outline=(91, 165, 255), width=5)
    draw.text((100, 145), "KNOWLEDGE REVIEW", font=font(34, True), fill=(125, 190, 255))
    draw.text((100, 220), f"{index:02d} / {total:02d}", font=font(26), fill=(180, 190, 210))
    body_font = font(64, True)
    lines = wrap_words(draw, text, body_font, WIDTH - 210)
    line_height = 88
    y = (HEIGHT - len(lines) * line_height) // 2
    for line in lines:
        box = draw.textbbox((0, 0), line, font=body_font)
        draw.text(((WIDTH - (box[2] - box[0])) // 2, y), line, font=body_font, fill=(250, 250, 255))
        y += line_height
    draw.rounded_rectangle((100, HEIGHT - 260, WIDTH - 100, HEIGHT - 190), radius=24, fill=(32, 48, 80))
    draw.text((130, HEIGHT - 245), label[:48], font=font(27, True), fill=(255, 220, 125))
    image.save(out_path, quality=92)


async def make_voice(text, path):
    communicate = edge_tts.Communicate(text, voice="en-US-AriaNeural", rate="+3%", volume="+0%")
    await communicate.save(str(path))


def run(cmd):
    subprocess.run(cmd, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)


def render_item(item, ffmpeg):
    slug = re.sub(r"[^a-z0-9]+", "-", item["id"].lower()).strip("-")
    work = OUT / f"work-{slug}"
    work.mkdir(parents=True, exist_ok=True)
    scenes = item.get("scenes", [])
    if not scenes or not item.get("title") or not item.get("source_notes"):
        raise ValueError(f"{item.get('id', 'item')}: title, scenes, and source_notes are required")
    # Only approved content is rendered. A source note is mandatory as an editorial safeguard.
    if item.get("review_status") != "approved":
        print(f"SKIP {slug}: review_status is not 'approved'")
        return
    narration = " ".join(scene["text"].strip() for scene in scenes)
    audio = work / "voice.mp3"
    asyncio.run(make_voice(narration, audio))
    clips = []
    for idx, scene in enumerate(scenes, 1):
        card = work / f"scene-{idx:02d}.png"
        draw_card(scene["text"], item["title"], card, idx, len(scenes))
        duration = max(3.0, len(scene["text"].split()) / 2.5)
        clip = work / f"scene-{idx:02d}.mp4"
        run([ffmpeg, "-y", "-loop", "1", "-i", str(card), "-t", str(duration),
             "-vf", f"scale={WIDTH}:{HEIGHT},format=yuv420p", "-r", str(FPS),
             "-c:v", "libx264", "-preset", "ultrafast", str(clip)])
        clips.append(clip)
    concat = work / "concat.txt"
    concat.write_text("".join(f"file '{p.as_posix()}'\n" for p in clips), encoding="utf-8")
    silent_video = work / "silent.mp4"
    run([ffmpeg, "-y", "-f", "concat", "-safe", "0", "-i", str(concat), "-c", "copy", str(silent_video)])
    final = OUT / f"{slug}.mp4"
    run([ffmpeg, "-y", "-i", str(silent_video), "-i", str(audio), "-shortest",
         "-c:v", "copy", "-c:a", "aac", "-b:a", "128k", "-movflags", "+faststart", str(final)])
    print(f"RENDERED {final}")


def main():
    ffmpeg = os.environ.get("FFMPEG_BIN", "ffmpeg")
    OUT.mkdir(exist_ok=True)
    data = json.loads(QUEUE.read_text(encoding="utf-8"))
    items = data.get("items", [])
    if not items:
        print("Queue is empty. Add researched, source-noted scripts with review_status='approved'.")
        return
    for item in items:
        try:
            render_item(item, ffmpeg)
        except Exception as exc:
            print(f"ERROR {item.get('id', 'unknown')}: {exc}")
            raise


if __name__ == "__main__":
    main()
