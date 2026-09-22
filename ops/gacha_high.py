# gacha_high.py - ve gacha CHAT LUONG CAO (anti-alias)
import os, math, random
import numpy as np
from PIL import Image, ImageDraw, ImageFilter
S = 4
W, H = 720 *  S, 1280 * S

def _c(x):
	return tuple(max(0,min(255,int(v))) for v in x)

def _shade(c, f):
	return _c(tuple(v * f for v in c))

def draw_hair_back(dr, cx, cy, r, hair):
	h2 = _shade(hair, 0.78)
	# toc sau dai mượt (nhieu lop)
	for i, off in enumerate([1.5, 1.3, 1.1]):
		dr.ellipse([cx-int(r * 1.3), cy-int(r * 0.9), cx+int(r * 1.3), cy+int(r * off * 1.6)], fill=_shade(hair, 0.6 + i * 0.1))
	# duoi toc dai xuong chan
	dr.polygon([(cx-int(r * 0.9), cy+int(r * 0.8)),(cx-int(r * 1.15), cy+int(r * 3.6)),(cx-int(r * 0.3), cy+int(r * 3.8)),(cx, cy+int(r * 1.0))], fill=hair)
	dr.polygon([(cx+int(r * 0.9), cy+int(r * 0.8)),(cx+int(r * 1.15), cy+int(r * 3.6)),(cx+int(r * 0.3), cy+int(r * 3.8)),(cx, cy+int(r * 1.0))], fill=hair)
	return dr


def draw_hair_front(dr, cx, cy, r, hair):
	h2 = _shade(hair, 0.85)
	h3 = _shade(hair, 1.2)
	# mai toc muot (2 lop)
	dr.pieslice([cx-int(r * 0.95), cy-int(r * 1.15), cx+int(r * 0.95), cy+int(r * 0.45)], 190, 350, fill=hair)
	dr.pieslice([cx-int(r * 0.85), cy-int(r * 0.95), cx+int(r * 0.85), cy+int(r * 0.2)], 200, 340, fill=h2)
	# highlight mai toc
	dr.arc([cx-int(r * 0.7), cy-int(r * 0.95), cx+int(r * 0.7), cy-int(r * 0.1)], 210, 330, fill=h3, width=int(r * 0.08))
	# toc ben mat
	dr.polygon([(cx-int(r * 0.9), cy-int(r * 1.0)),(cx-int(r * 1.1), cy+int(r * 1.2)),(cx-int(r * 0.75), cy+int(r * 1.0))], fill=hair)
	dr.polygon([(cx+int(r * 0.9), cy-int(r * 1.0)),(cx+int(r * 1.1), cy+int(r * 1.2)),(cx+int(r * 0.75), cy+int(r*1.0))], fill=hair)
	return dr

def draw_face_hd(dr, cx, cy, r, skin):
	sh = _shade(skin, 0.9)
	# mat oval anime
	dr.ellipse([cx-int(r * 0.82), cy-int(r * 0.95), cx+int(r * 0.82), cy+int(r * 1.02)], fill=skin)
	# cam nho
	dr.polygon([(cx-int(r * 0.06), cy+int(r * 0.2)),(cx+int(r * 0.06), cy+int(r * 0.2)),(cx, cy+int(r * 0.28))], fill=sh)
	# mieng
	dr.arc([cx-int(r * 0.22), cy+int(r * 0.42), cx+int(r * 0.22), cy+int(r * 0.68)], 10, 170, fill=(200,90,100), width=int(r * 0.05))
	# blush
	dr.ellipse([cx-int(r * 0.72), cy+int(r * 0.28), cx-int(r * 0.42), cy+int(r * 0.52)], fill=(255,175,185))
	dr.ellipse([cx+int(r * 0.42), cy+int(r * 0.28), cx+int(r * 0.72), cy+int(r * 0.52)], fill=(255,175,185))
	return dr


def draw_eyes_hd(dr, cx, cy, r, eye):
	ew = int(r * 0.3); eh = int(r * 0.4)
	top = _shade(eye, 0.55); bot = _shade(eye, 1.15)
	for s in (-1, 1):
		ex = cx + s * int(r * 0.4)
		dr.ellipse([ex-ew, cy-eh, ex+ew, cy+eh], fill=(255,255,255))
		iw = int(ew * 0.92); ih = int(eh * 0.92)
		# iris gradient (ve nhieu vong)
		for k in range(8):
			f = k / 8.0
			rr = int(iw * (1 - f * 0.15))
			col = _c((top[0]+(bot[0]-top[0]) * f, top[1]+(bot[1]-top[1]) * f, top[2]+(bot[2]-top[2]) * f))
			dr.ellipse([ex-rr, cy-ih+int(ih * 2*f*0.3), ex+rr, cy+ih], fill=col)
		# pupil
		pr = int(iw * 0.4)
		dr.ellipse([ex-pr, cy-pr, ex+pr, cy+pr], fill=(28,22,38))
		# highlight lon
		h1 = int(iw * 0.5)
		dr.ellipse([ex-iw+2, cy-ih+2, ex-iw+2+h1, cy-ih+2+h1], fill=(255,255,255))
		# highlight nho
		h2 = int(iw * 0.25)
		dr.ellipse([ex+iw-h2 * 2-2, cy+ih-h2 * 2-2, ex+iw-2, cy+ih-2], fill=(255,255,255))
		# long mi tren
		dr.arc([ex-ew-int(r * 0.05), cy-eh-int(r * 0.1), ex+ew+int(r * 0.05), cy+eh], 200, 340, fill=(55,38,52), width=int(r * 0.07))
	return dr

def draw_ears(dr, cx, cy, r, hair, kind):
	h2 = _shade(hair, 0.8)
	if kind == 'catear':
		for s in (-1,1):
			bx = cx + math.sin(r * 0.5)
			dr.polygon([(bx, cy-int(r * 0.95)),(bx-math.sin(r * 0.32), cy-int(r * 1.55)),(bx+math.sin(r * 0.18), cy-int(r * 1.35))], fill=hair)
			dr.polygon([(bx, cy-int(r * 1.0)),(bx-math.sin(r * 0.18), cy-int(r * 1.38)),(bx+math.sin(r * 0.08), cy-int(r * 1.25))], fill=(255,190,200))
	elif kind == 'bunny':
		for s in (-1,1):
			bx = cx + math.sin(r * 0.4)
			dr.ellipse([bx-int(r * 0.16), cy-int(r * 1.8), bx+int(r * 0.16), cy-int(r * 0.95)], fill=hair)
			dr.ellipse([bx-int(r * 0.08), cy-int(r * 1.7), bx+int(r * 0.08), cy-int(r * 1.1)], fill=(255,200,210))
	return dr


def draw_outfit(dr, cx, cy, r, skin, top, bottom, sock):
	# co + vai
	dr.rectangle([cx-int(r * 0.16), cy+int(r * 0.95), cx+int(r * 0.16), cy+int(r * 1.15)], fill=_shade(skin,0.95))
	# ao crop top
	dr.rounded_rectangle([cx-int(r * 0.5), cy+int(r * 1.08), cx+int(r * 0.5), cy+int(r * 1.75)], radius=int(r * 0.12), fill=top)
	# tay ao hong (long)
	for s in (-1,1):
		ax = cx + math.sin(r * 0.58)
		dr.rounded_rectangle([ax-int(r * 0.14), cy+int(r * 1.1), ax+int(r * 0.14), cy+int(r * 1.55)], radius=int(r * 0.1), fill=bottom)
		dr.ellipse([ax-int(r * 0.15), cy+int(r * 1.5), ax+int(r * 0.15), cy+int(r * 1.75)], fill=skin)
	# quan/vay
	dr.rounded_rectangle([cx-int(r * 0.48), cy+int(r * 1.72), cx+int(r * 0.48), cy+int(r * 2.2)], radius=int(r * 0.1), fill=bottom)
	# chan + tat
	for s in (-1,1):
		lx = cx + math.sin(r * 0.24)
		dr.rounded_rectangle([lx-int(r * 0.13), cy+int(r * 2.18), lx+int(r * 0.13), cy+int(r * 2.8)], radius=int(r * 0.09), fill=skin)
		dr.rounded_rectangle([lx-int(r * 0.14), cy+int(r * 2.3), lx+int(r * 0.14), cy+int(r * 2.68)], radius=int(r * 0.08), fill=sock)
		dr.rounded_rectangle([lx-int(r * 0.15), cy+int(r * 2.78), lx+int(r * 0.17), cy+int(r * 2.95)], radius=int(r * 0.06), fill=(35,35,45))
	return dr

def draw_tail_hd(dr, cx, cy, r, hair):
	h2 = _shade(hair, 0.85)
	dr.ellipse([cx-int(r * 1.7), cy+int(r * 1.6), cx-int(r * 0.55), cy+int(r * 2.9)], fill=hair)
	dr.ellipse([cx-int(r * 1.45), cy+int(r * 1.75), cx-int(r * 0.75), cy+int(r * 2.7)], fill=h2)
	return dr


def draw_character(dr, cx, cy, r, p, mouth_open=1.0):
	draw_tail_hd(dr, cx, cy, r, p['hair'])
	draw_hair_back(dr, cx, cy, r, p['hair'])
	draw_outfit(dr, cx, cy, r, p['skin'], p['top'], p['bottom'], p['sock'])
	draw_face_hd(dr, cx, cy, r, p['skin'])
	draw_eyes_hd(dr, cx, cy, r, p['eye'])
	draw_ears(dr, cx, cy, r, p['hair'], p['ears'])
	draw_hair_front(dr, cx, cy, r, p['hair'])
	return dr

def make_char(seed=0):
	random.seed(seed)
	hair = random.choice([(255,140,190),(255,105,180),(255,170,210),(150,90,200)])
	skin = random.choice([(255,228,205),(250,218,195)])
	eye = random.choice([(255,90,150),(190,70,160),(120,90,220)])
	top = (40,40,60)
	bottom = random.choice([(255,140,190),(255,160,200)])
	sock = random.choice([(255,140,190),(255,180,210)])
	ears = random.choice(['catear', 'bunny'])
	return {'hair': hair, 'skin': skin, 'eye': eye, 'top': top, 'bottom': bottom, 'sock': sock, 'ears': ears}

def render_frame(p, t):
	random.seed(42)
	img = Image.new('RGB', (W, H), (180,220,255))
	dr = ImageDraw.Draw(img)
	for y in range(0, int(H * 0.62), 4):
		f = y / (H * 0.62)
		dr.rectangle([0, y, W, y+4], fill=_c((120 + 80 * f, 180 + 60 * f, 255 - 20 * f)))
	dr.rectangle([0,int(H * 0.62),W,H], fill=(120,200,110))
	for _ in range(18):
		fx=random.randint(0,W); fy=random.randint(int(H * 0.6),H); fr = random.randint(3,7) * S
		dr.ellipse([fx-fr,fy-fr,fx+fr,fy+fr], fill=random.choice([(255,180,200),(255,220,120),(255,255,255)]))
	bob = math.sin(t * 3) * int(14 * S)
	draw_character(dr, W//2, int(H * 0.36) + bob, int(230 * S), p)
	return img.resize((720, 1280), Image.LANCZOS)
def make_video(out, dur, seed=0, fps=30):
	os.environ['IMAGEIO_FFMPEG_EXE'] = os.path.abspath(os.path.join(os.getcwd(), 'tools', 'ffmpeg.exe'))
	p = make_char(seed)
	from moviepy.video.VideoClip import VideoClip
	def mk(t):
		return np.array(render_frame(p, t))
	clip = VideoClip(mk)
	clip = clip.set_duration(dur) if hasattr(clip,'set_duration') else clip.with_duration(dur)
	clip = clip.set_fps(fps) if hasattr(clip,'set_fps') else clip.with_fps(fps)
	clip.write_videofile(out, fps=fps, codec='libx264', preset='veryfast', audio=False, logger=None)
	return out
