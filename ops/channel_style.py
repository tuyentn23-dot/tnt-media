# channel_style.py - Build short video with per-channel style.
import os, sys, io, json, random, hashlib
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)
os.environ['IMAGEIO_FFMPEG_EXE'] = os.path.join(ROOT, 'tools', 'ffmpeg.exe')

import numpy as np
from PIL import Image, ImageDraw, ImageFont

FONT = os.path.join(ROOT, 'tools', 'font.ttf')
TARGET = 58.0


def _hex_to_rgb(h):
	h = (h or '#ffffff').lstrip('#')
	if len(h) == 3:
		h = ''.join([c*2 for c in h])
	return tuple(int(h[i:i+2], 16) for i in (0, 2, 4))


def _wrap(draw, text, font, maxw):
	words = text.split()
	lines = []
	cur = ''
	for w in words:
		test = (cur + ' ' + w).strip()
		if draw.textlength(test, font=font) <= maxw:
			cur = test
		else:
			if cur:
				lines.append(cur)
			cur = w
	if cur:
		lines.append(cur)
	return lines


def text_frame(text, fs, color, font_path, W=720, H=1280, y=300, stroke=4):
	img = Image.new('RGBA', (W, H), (0, 0, 0, 0))
	dr = ImageDraw.Draw(img)
	try:
		font = ImageFont.truetype(font_path, fs)
	except Exception:
		font = ImageFont.truetype(FONT, fs)
	lines = _wrap(dr, text, font, W - 80)
	lh = fs + 10
	cy = y
	for ln in lines:
		w = dr.textlength(ln, font=font)
		x = (W - w) / 2
		dr.text((x, cy), ln, font=font, fill=color, stroke_width=stroke, stroke_fill='black')
		cy += lh
	return np.array(img)


def build_styled(item, out, style=None, seed=None):
	style = style or {}
	from ops.compat import get_audio_clip, concat as cc
	from ops import content_video5 as cv5
	A = get_audio_clip()
	cid = item.get('id', 'x')
	vo = os.path.join(ROOT, 'output', 'vo_ch' + cid + '.mp3')
	text_full = item['hook'] + ' ' + item['body'] + ' ' + item.get('payoff', '')
	cv5.tts(text_full, vo)
	aud = A(vo)
	if aud.duration > TARGET:
		aud = aud.subclip(0, TARGET)
	cs = []
	_topic = str(item.get("topic", "")).strip().lower()
	if _topic:
		_d = os.path.join(ROOT, "library", _topic)
		if os.path.isdir(_d):
			cs = [os.path.join(_d, f) for f in sorted(os.listdir(_d)) if f.lower().endswith(".mp4")]
	# FALLBACK: neu topic khong co footage, quet toan bo library
	if not cs:
		_lib = os.path.join(ROOT, "library")
		_all = []
		if os.path.isdir(_lib):
			for _sub in sorted(os.listdir(_lib)):
				_sp = os.path.join(_lib, _sub)
				if os.path.isdir(_sp):
					_all.extend([os.path.join(_sp, f) for f in sorted(os.listdir(_sp)) if f.lower().endswith(".mp4") and not f.startswith("music")])
		if _all:
			_h = int(hashlib.md5(str(item.get("id", "x")).encode()).hexdigest()[:6], 16)
			_take = min(6, len(_all))
			_start = _h % max(1, len(_all) - _take + 1)
			cs = _all[_start:_start + _take]
	if seed is None:
		seed = int(hashlib.md5(cid.encode()).hexdigest()[:6], 16)
	random.seed(seed)
	if cs:
		random.shuffle(cs)
	W, H = 720, 1280
	aspect = style.get('aspect', '9:16')
	if aspect == '1:1':
		W, H = 1080, 1080
	elif aspect == '16:9':
		W, H = 1280, 720
	color_primary = _hex_to_rgb(style.get('color_primary', '#1a1a2e'))
	color_accent = _hex_to_rgb(style.get('color_accent', '#e94560'))
	fs = int(style.get('font_size', 44))  # caption nho, dat thap
	font_path = FONT
	wm = style.get('watermark', '')
	segments = []
	n = max(1, int(aud.duration / 3))
	texts = [item['hook'], item['body'], item.get('payoff', '')]
	for i in range(n):
		cpath = cs[i % len(cs)] if cs else None
		txt = texts[min(i, len(texts) - 1)]
		# Caption dat thap (vung an toan duoi), chu nho, khong che hinh
		y = int(H * 0.68)
		clip = cv5.make_scene(cpath, txt, color_accent, fs, aud.duration / n, y, seed=seed + i)
		segments.append(clip)
	body = cc(segments) if len(segments) > 1 else segments[0]
	body = (body.with_duration(aud.duration).with_audio(aud) if hasattr(body, "with_duration") else body.set_duration(aud.duration).set_audio(aud))
	if wm:
		overlay = text_frame(wm, max(28, fs // 2), color_primary, font_path, W=W, H=H, y=H - 140)
		from ops.compat import get_image_clip, composite
		wm_clip = get_image_clip()(overlay, duration=body.duration)
		body = composite([body, wm_clip])
	body.write_videofile(out, fps=30, codec='libx264', audio_codec='aac', logger=None)
	return out


if __name__ == '__main__':
	print('channel_style ready. FONT=', FONT, 'exists=', os.path.exists(FONT))
