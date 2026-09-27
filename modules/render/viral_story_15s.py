# -*- coding: utf-8 -*-
import os
import subprocess
import tempfile
from ops import voice_synth as VS
from ops import voice_engine as VE

MODULE = {"name": "render.viral_story_15s", "version": "1.0.0", "health": True, "interface": "run(ctx)"}
W, H, FPS = 1080, 1920, 30
FONT = os.path.abspath("tools/font_arial.ttf")

def _ffpath(path):
 from ops.ffmpeg_render import ffpath
 return ffpath(path)

def _drawtext(textfile, start, end, y, fs, color="white"):
    q = "'"
    s = "drawtext=fontfile=" + _ffpath(FONT) + ":textfile=" + _ffpath(textfile)
    s += ":enable=" + q + "between(t," + str(start) + "," + str(end) + ")" + q
    s += ":fontsize=" + str(fs) + ":fontcolor=" + color
    s += ":borderw=4:bordercolor=black:line_spacing=12:text_align=C"
    s += ":x=(w-text_w)/2:y=" + str(y)
    return s

def render(item, out, style=None):
    st = style or {}
    src = os.path.abspath(item["footage"])
    out = os.path.abspath(out)
    if not os.path.exists(src):
        raise FileNotFoundError(src)
    os.makedirs(os.path.dirname(out), exist_ok=True)
    base = os.path.join(os.getcwd(), 'work')
    os.makedirs(base, exist_ok=True)
    td = tempfile.mkdtemp(prefix='viralstory_', dir=base)
    voice = os.path.join(td, "voice.mp3")
    VS.synth_parts(
        item["voice_parts"],
        voice,
        voice=st.get("voice", "female_north"),
        preset=st.get("preset", st.get("voice_preset", "cute")),
        gap=0.28,
    )
    titlef = os.path.join(td, "title.txt")
    open(titlef, "w", encoding="utf-8").write(item["title"])
    filters = ["scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,fps=30"]
    filters.append(_drawtext(titlef, 0, 1.4, "0.12*h", 58, "0xFFEB3B"))
    for i, cap in enumerate(item["captions"]):
        start, end, text = cap
        fp = os.path.join(td, "cap" + str(i) + ".txt")
        open(fp, "w", encoding="utf-8").write(text)
        filters.append(_drawtext(fp, start, end, "0.67*h", 62, "white"))
    filters.append("drawbox=x=0:y=h-16:w=iw*(t/15):h=16:color=0xe94560@0.85:t=fill")
    cmd = [
        VE.FFMPEG, "-y", "-stream_loop", "-1", "-i", src, "-i", voice,
        "-t", "15", "-vf", ",".join(filters),
        "-map", "0:v:0", "-map", "1:a:0",
        "-c:v", "libx264", "-preset", "veryfast", "-crf", "20",
        "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "192k", out,
    ]
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode != 0:
        raise RuntimeError(r.stderr)
    return out
