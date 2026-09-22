# content_video5.py - shorts renderer (moviepy v2.1.x + PIL text)
import os, sys, json, glob, numpy as np
from PIL import Image, ImageDraw, ImageFont
if not hasattr(Image, "ANTIALIAS"):
	Image.ANTIALIAS = Image.LANCZOS
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)
DB = os.path.join(ROOT, "memory", "content_db.json")
FONT = "C:/Windows/Fonts/arialbd.ttf"
TARGET = 13.0


def load(kind):
	return json.load(open(DB, encoding="utf-8")).get(kind, [])


def _wrap(draw, text, font, maxw):
	words = text.split()
	lines = []
	cur = ""
	for w in words:
		test = (cur + " " + w).strip()
		if draw.textlength(test, font=font) <= maxw:
			cur = test
		else:
			if cur:
				lines.append(cur)
			cur = w
	if cur:
		lines.append(cur)
	return lines


def text_frame(text, fs, color, W=720, H=1280, y=300):
	img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
	dr = ImageDraw.Draw(img)
	font = ImageFont.truetype(FONT, fs)
	lines = _wrap(dr, text, font, W - 80)
	lh = fs + 12
	cy = y
	for ln in lines:
		w = dr.textlength(ln, font=font)
		x = (W - w) / 2
		dr.text((x, cy), ln, font=font, fill=color, stroke_width=4, stroke_fill="black")
		cy += lh
	return np.array(img)


def make_scene(cpath, text, color, fs, dur, y, seed=0):
	from ops.compat import get_video_clip, concat as cc
	from ops.compat import _editor as _cmp_editor
	ColorClip = _cmp_editor()[5]
	from moviepy.video.VideoClip import VideoClip
	V = get_video_clip()
	if cpath:
		_c = V(cpath)
		b = (_c.resized(height=1280) if hasattr(_c, "resized") else _c.resize(height=1280))
	else:
		b = ColorClip((720, 1280), color=(8, 10, 25), duration=dur)
	if b.w >= 720:
		b = (b.cropped(width=720, x_center=b.w / 2) if hasattr(b, "cropped") else b.crop(x1=(b.w-720)//2, width=720))
	else:
		b = (b.resized(width=720) if hasattr(b, "resized") else b.resize(width=720))
	if b.h < 1280:
		b = b.resized(height=1280)
	if b.duration < dur:
		n = int(dur / b.duration) + 1
		b = cc([b] + [b] * (n - 1))
	b = (b.subclipped(0, dur) if hasattr(b, "subclipped") else b.subclip(0, dur))
	b = (b.cropped(width=720, height=1280, x_center=b.w / 2, y_center=b.h / 2) if hasattr(b, "cropped") else b.crop(x1=(b.w-720)//2, y1=(b.h-1280)//2, width=720, height=1280))
	col = (255, 255, 0) if color == "yellow" else ((0, 255, 204) if color == "#00ffcc" else (255, 255, 255))
	overlay = text_frame(text, fs, col, 720, 1280, y)
	def mk(get, t):
		fr = get(t)
		ov = overlay.astype("float32") / 255.0
		fr = fr.astype("float32")
		out = fr * (1 - ov[..., 3:4]) + ov[..., :3] * 255 * ov[..., 3:4]
		return out.astype("uint8")
	vid = VideoClip(lambda t: mk(b.get_frame, t))
	vid = (vid.with_duration(dur).with_fps(30) if hasattr(vid, "with_fps") else vid.set_fps(30).set_duration(dur))
	return vid


def tts(text, out):
	from gtts import gTTS
	gTTS(text=text, lang="vi").save(out)


def build(item, out, seed=None):
	from ops.compat import get_audio_clip, concat as cc
	import random, hashlib
	A = get_audio_clip()
	os.makedirs(os.path.join(ROOT, "output"), exist_ok=True)
	vo = os.path.join(ROOT, "output", "vo5" + item["id"] + ".mp3")
	tts(item["hook"] + " " + item["body"] + " " + item["payoff"], vo)
	aud = A(vo)
	if aud.duration > TARGET:
		aud = aud.subclipped(0, min(TARGET, aud.duration))
	parts = [(item["hook"], "yellow", 56, 300), (item["body"], "white", 44, 560), (item["payoff"], "#00ffcc", 48, 900)]
	seg = min(aud.duration, TARGET) / 3.0
	scenes = []
	for i, (tx, col, fs, y) in enumerate(parts):
		scenes.append(make_scene(None, tx, col, fs, seg, y, seed=(seed or 0) + i))
	vid = cc(scenes)
	vid = vid.with_audio(aud)
	vid.write_videofile(out, fps=30, codec="libx264", audio_codec="aac", logger=None)
	return out