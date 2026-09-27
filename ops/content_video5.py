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


def text_frame(text, fs, color, W=540, H=960, y=225):
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




# make_scene v3 - co fallback neu clip corrupt

def make_scene(cpath, text, color, fs, dur, y, seed=0):
	from ops.compat import get_video_clip, concat as cc
	from ops.compat import _editor as _cmp_editor
	ColorClip = _cmp_editor()[5]
	from moviepy.video.VideoClip import VideoClip
	from PIL import Image
	import numpy as np
	V = get_video_clip()
	col = (255, 255, 0) if color == 'yellow' else ((0, 255, 204) if color == '#00ffcc' else (255, 255, 255))
	overlay = text_frame(text, fs, col, 540, 960, y)
	if not isinstance(overlay, Image.Image):
		overlay = Image.fromarray(overlay).convert('RGBA')
	_c = None
	if cpath:
		try:
			try:
				_c = V(cpath, target_resolution=(360, 640), audio=False)
			except Exception:
				_c = V(cpath, target_resolution=(360, 640), audio=False)
			_ = _c.get_frame(0)
		except Exception as e:
			print('[make_scene] clip fail:', cpath, str(e)[:100])
			_c = None
	if _c is None:
		_c = ColorClip((540, 960), color=(8, 10, 25), duration=dur)
	def mk(get, t):
		try:
			fr = get(t)
		except Exception:
			fr = np.zeros((960, 540, 3), dtype=np.uint8)
		if fr.dtype != np.uint8:
			fr = fr.astype(np.uint8)
		img = Image.fromarray(fr)
		if img.mode != "RGB":
			img = img.convert("RGB")
		if img.size != (540, 960):
			img = img.resize((540, 960), Image.LANCZOS)
		img.paste(overlay, (0, 0), overlay)
		return np.asarray(img, dtype=np.uint8)
	vid = VideoClip(lambda t: mk(_c.get_frame, t))
	vid = (vid.with_duration(dur).with_fps(30) if hasattr(vid, 'with_fps') else vid.set_fps(30).set_duration(dur))
	return vid



def tts(text, out, voice=None, preset=None):
	try:
		from ops import voice_engine as VE
		v = voice or chr(102)+chr(101)+chr(109)+chr(97)+chr(108)+chr(101)+chr(95)+chr(110)+chr(111)+chr(114)+chr(116)+chr(104)
		pr = preset or chr(115)+chr(116)+chr(111)+chr(114)+chr(121)
		VE.tts(text, out, voice=v, preset=pr, pause_ms=200)
		if os.path.exists(out) and os.path.getsize(out) > 1000:
			return out
	except Exception as e:
		print(chr(91)+chr(116)+chr(116)+chr(115)+chr(93), str(e)[:80])
	try:
		from ops import voice_synth
		voice_synth.synth(text, out, voice=chr(102)+chr(101)+chr(109)+chr(97)+chr(108)+chr(101)+chr(95)+chr(110)+chr(111)+chr(114)+chr(116)+chr(104), preset=chr(115)+chr(116)+chr(111)+chr(114)+chr(121), maxlen=4000)
		if os.path.exists(out) and os.path.getsize(out) > 1000:
			return out
	except Exception:
		pass
	from gtts import gTTS
	gTTS(text=text, lang=chr(118)+chr(105)).save(out)
	return out

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