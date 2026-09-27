# channel_style.py - Build short video with per-channel style.
import os, sys, io, json, random, hashlib
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(file)))
sys.path.insert(0, ROOT)
os.environ['IMAGEIO_FFMPEG_EXE'] = os.path.join(ROOT, 'tools', 'ffmpeg.exe')
import numpy as np
from PIL import Image, ImageDraw, ImageFont

FONT = os.path.join(ROOT, 'tools', 'font.ttf')
TARGET = 58.0


def _hex_to_rgb(h):
	h = (h or '#ffe000').lstrip('#')
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


def text_frame(text, fs, color, font_path, W=720, H=1280, y=300):
	img = Image.new('RGBA', (W, H), (0, 0, 0, 0))
	dr = ImageDraw.Draw(img)
	try:
		font = ImageFont.truetype(font_path, fs)
	except Exception:
		font = ImageFont.truetype(FONT, fs)
	lines = wrap(dr, text, font, W - 80)
	lh = fs + 12
	cy = y
	for ln in lines:
		w = dr.textlength(ln, font=font)
		x = (W - w) / 2
		dr.text((x, cy), ln, font=font, fill=color, stroke_width=4, stroke_fill='black')
		cy += lh
	return np.array(img)


def pick_footage(topic, k=8):
	base = os.path.join(ROOT, 'library')
	topic = (topic or '').strip().lower()
	fs = []
	d = os.path.join(base, topic)
	if topic and os.path.isdir(d):
	fs = [os.path.join(d, f) for f in sorted(os.listdir(d)) if f.lower().endswith('.mp4')]
	if not fs and os.path.isdir(base):
	for sub in sorted(os.listdir(base)):
	sp = os.path.join(base, sub)
	if os.path.isdir(sp):
	fs.extend([os.path.join(sp, f) for f in sorted(os.listdir(sp)) if f.lower().endswith('.mp4')])
	if not fs:
	return []
	h = int(hashlib.md5(str(topic).encode()).hexdigest()[:6], 16)
	start = h % max(1, len(fs) - k + 1)
	return fs[start:start + k]


def build_styled(item, out, style=None, seed=None):
	style = style or {}
	from ops.compat import get_audio_clip, concat as cc
	from ops import content_video5 as cv5
	A = get_audio_clip()
	cid = str(item.get('id', 'x'))
	vo = os.path.join(ROOT, 'output', 'vo_ch' + cid + '.mp3')
	secs = [item.get('hook', ''), item.get('body', ''), item.get('payoff', '')]
	try:
	from ops import voice_synth as vsx
	vsx.synth_sections(secs, vo, voice='female_north', preset='hype', gap=0.5)
	except Exception:
	cv5.tts(' '.join(secs), vo)
	aud_src = vo
	try:
	from ops import music_mixer as mmx
	mixed = os.path.join(ROOT, 'output', 'mixed' + cid + '.wav')
	mmx.mix_for(cid, vo, topic=str(item.get('topic', '')), out=mixed, duck=True)
	if os.path.exists(mixed) and os.path.getsize(mixed) > 2000:
	aud_src = mixed
	except Exception:
	aud_src = vo
	aud = A(aud_src)
	if aud.duration > TARGET:
	aud = aud.subclip(0, TARGET)
	dur = float(aud.duration)
	topic = str(item.get('topic', '')).strip().lower()
	cs = pick_footage(topic, k=8)
	W, H = 720, 1280
	fs = int(style.get('font_size', 48))
	color = _hex_to_rgb(style.get('color_accent', '#ffe000'))
	if seed is None:
	seed = int(hashlib.md5(cid.encode()).hexdigest()[:6], 16)
	random.seed(seed)
	texts = [secs[0], secs[1], secs[2] if secs[2] else secs[1]]
	segments = []
	plan = None
	try:
	from ops import beat_sync as bsx
	beats = bsx.detect_beats(aud_src, dur=dur)
	if cs:
	plan = bsx.beat_sync(cs, beats, dur)
	except Exception:
	plan = None
	if plan:
	for i, (c, s, d) in enumerate(plan):
	txt = texts[min(i, len(texts) - 1)]
	segments.append(cv5.make_scene(c, txt, color, fs, d, int(H * 0.66), seed=seed + i))
	else:
	n = max(3, len([t for t in secs if t]))
	seg = dur / float(n)
	for i in range(n):
	c = cs[i % len(cs)] if cs else None
	txt = texts[min(i, len(texts) - 1)]
	segments.append(cv5.make_scene(c, txt, color, fs, seg, int(H * 0.66), seed=seed + i))
	body = cc(segments) if len(segments) > 1 else segments[0]
	if hasattr(body, 'with_duration'):
	body = body.with_duration(aud.duration).with_audio(aud)
	else:
	body = body.set_duration(aud.duration).set_audio(aud)
	body.write_videofile(out, fps=30, codec='libx264', audio_codec='aac', logger=None)
	return out
