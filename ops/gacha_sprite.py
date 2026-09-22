# gacha_sprite.py - ve nhan vat gacha theo LAYER chi tiet (tab)
import os, math, random
import numpy as np
from PIL import Image, ImageDraw, ImageFilter
W, H = 720, 1280

def _shade(c, f):
	return tuple(max(0,min(255,int(x * f))) for x in c)

def _rr(dr, box, r, **kw):
	dr.rounded_rectangle(box, radius=r, **kw)

def draw_face(dr, cx, cy, r, skin):
	# mat chinh (oval anime)
	dr.ellipse([cx-int(r * 0.85), cy-r, cx+int(r * 0.85), cy+int(r * 1.05)], fill=skin)
	# cam
	dr.polygon([(cx-int(r * 0.12), cy+int(r * 0.15)),(cx+int(r * 0.12), cy+int(r * 0.15)),(cx, cy+int(r * 0.28))], fill=_shade(skin, 0.9))
	# mieng cuoi
	dr.arc([cx-int(r * 0.25), cy+int(r * 0.4), cx+int(r * 0.25), cy+int(r * 0.7)], 0, 180, fill=(180,80,90), width=4)
	return dr

def draw_eyes(dr, cx, cy, r, eye):
	ew = int(r *  0.32); eh = int(r *  0.4)
	for s in (-1, 1):
		ex = cx + s * int(r *  0.38)
		# long trang
		dr.ellipse([ex-ew, cy-eh, ex+ew, cy+eh], fill=(255,255,255))
		# iris (gradient)
		iw = int(ew *  0.9); ih = int(eh *  0.9)
		dr.ellipse([ex-iw, cy-ih, ex+iw, cy+ih], fill=_shade(eye, 0.7))
		dr.ellipse([ex-iw, cy-int(ih * 0.2), ex+iw, cy+ih], fill=eye)
		dr.ellipse([ex-iw, cy+int(ih * 0.3), ex+iw, cy+ih], fill=_shade(eye, 0.5))
		# pupil
		pr = int(iw *  0.45)
		dr.ellipse([ex-pr, cy-pr, ex+pr, cy+pr], fill=(30,25,40))
		# highlight lon tren
		h1 = int(iw *  0.5)
		dr.ellipse([ex-iw, cy-ih, ex-iw+h1 * 2, cy-ih+h1 * 2], fill=(255,255,255))
		# highlight nho duoi
		h2 = int(iw *  0.28)
		dr.ellipse([ex+iw-h2*2, cy+ih-h2*2, ex+iw, cy+ih], fill=(255,255,255))
		# long mi tren
		dr.arc([ex-ew, cy-eh-int(r * 0.15), ex+ew, cy+eh], 200, 340, fill=(60,40,55), width=6)
	# long may
	for s in (-1, 1):
		ex = cx + s * int(r *  0.38)
		dr.arc([ex-ew, cy-eh-int(r * 0.35), ex+ew, cy-eh-int(r *  0.05)], 200, 340, fill=(70,50,60), width=5)
	return dr

def draw_hair(dr, cx, cy, r, hair, style):
	h2 = _shade(hair,  0.72)
	h3 = _shade(hair, 1.15)
	# toc sau dai
	dr.ellipse([cx-int(r * 1.25), cy-int(r * 1.1), cx+int(r * 1.25), cy+int(r * 1.9)], fill=h2)
	# mai toc (fringe)
	dr.pieslice([cx-int(r * 0.9), cy-int(r * 1.15), cx+int(r * 0.9), cy+int(r * 0.35)], 190, 350, fill=hair)
	dr.pieslice([cx-int(r * 0.9), cy-int(r * 0.9), cx+int(r * 0.9), cy+int(r * 0.1)], 200, 340, fill=h3)
	# twin tails
	if style == 'twin':
		for s in (-1,1):
			tx = cx + math.sin(r * 1.1)
			dr.ellipse([tx-int(r * 0.45), cy-int(r * 0.9), tx+int(r * 0.45), cy+int(r * 1.6)], fill=hair)
	# bunny/cat ears
	if style == 'catear':
		for s in (-1,1):
			ex = cx + math.sin(r * 0.55)
			dr.polygon([(ex, cy-int(r * 0.95)),(ex-math.sin(r * 0.3), cy-int(r * 1.5)),(ex+math.sin(r * 0.12), cy-int(r * 1.35))], fill=hair)
			dr.polygon([(ex, cy-int(r * 1.0)),(ex-math.sin(r * 0.16), cy-int(r * 1.35)),(ex+math.sin(r * 0.05), cy-int(r * 1.25))], fill=(255,190,200))
	return dr

def draw_body(dr, cx, cy, r, skin, top, bottom):
	# co
	dr.rectangle([cx-int(r * 0.18), cy+int(r * 0.9), cx+int(r * 0.18), cy+int(r * 1.15)], fill=skin)
	# ao tren
	dr.rounded_rectangle([cx-int(r * 0.55), cy+int(r * 1.1), cx+int(r * 0.55), cy+int(r * 1.8)], radius=int(r * 0.15), fill=top)
	# tay
	for s in (-1,1):
		ax = cx + math.sin(r * 0.62)
		dr.rounded_rectangle([ax-int(r * 0.13), cy+int(r * 1.15), ax+int(r * 0.13), cy+int(r * 1.75)], radius=int(r * 0.1), fill=top)
		dr.ellipse([ax-int(r * 0.13), cy+int(r * 1.72), ax+int(r * 0.13), cy+int(r * 1.98)], fill=skin)
	# quan/vay
	dr.rounded_rectangle([cx-int(r * 0.5), cy+int(r * 1.78), cx+int(r * 0.5), cy+int(r * 2.3)], radius=int(r * 0.1), fill=bottom)
	# chan
	for s in (-1,1):
		lx = cx + math.sin(r * 0.25)
		dr.rounded_rectangle([lx-int(r * 0.* 14), cy+int(r * 2.28), lx+int(r * 0.* 14), cy+int(r * 2.95)], radius=int(r * 0.1), fill=skin)
		dr.rounded_rectangle([lx-int(r * 0.15), cy+int(r * 2.4), lx+int(r * 0.15), cy+int(r * 2.75)], radius=int(r * 0.08), fill=bottom)
		# giay
		dr.rounded_rectangle([lx-int(r * 0.16), cy+int(r * 2.9), lx+int(r * 0.16), cy+int(r * 3.05)], radius=int(r * 0.06), fill=(40,40,50))
	return dr

def draw_tail(dr, cx, cy, r, hair, tail_type):
	h2 = _shade(hair, 0.8)
	if tail_type == 'fluffy':
		# duoi to xum
		dr.ellipse([cx-int(r * 1.5), cy+int(r * 1.8), cx-int(r * 0.5), cy+int(r * 2.6)], fill=hair)
		dr.ellipse([cx-int(r * 1.3), cy+int(r * 1.9), cx-int(r * 0.6), cy+int(r * 2.5)], fill=h2)
	elif tail_type == 'cat':
		dr.arc([cx+int(r * 0.3), cy+int(r * 1.6), cx+int(r * 1.6), cy+int(r * 2.8)], 90, 270, fill=hair, width=int(r * 0.15))
	return dr


def draw_char(dr, cx, cy, r, skin, hair, eye, top, bottom, style, tail_type, pose='stand'):
	draw_tail(dr, cx, cy, r, hair, tail_type)
	draw_body(dr, cx, cy, r, skin, top, bottom)
	draw_face(dr, cx, cy, r, skin)
	draw_eyes(dr, cx, cy, r, eye)
	# blush
	dr.ellipse([cx-int(r * 0.72), cy+int(r * 0.3), cx-int(r * 0.48), cy+int(r * 0.5)], fill=(255,180,190))
	dr.ellipse([cx+int(r * 0.48), cy+int(r * 0.3), cx+int(r * 0.72), cy+int(r *  0.5)], fill=(255,180,190))
	draw_hair(dr, cx, cy, r, hair, style)
	return dr

HAIRS=[(255,140,190),(255,105,180),(150,80,200),(255,180,200),(220,70,120),(120,180,255),(255,200,120)]
SKINS=[(255,228,205),(248,215,190),(230,195,170)]
EYES=[(255,90,150),(120,90,220),(90,200,180),(255,160,60),(180,70,160)]
TOPS=[(40,40,60),(200,80,120),(80,150,220),(60,60,90)]
BOTTOMS=[(255,140,190),(120,90,200),(255,200,100),(90,180,220)]
STYLES=['twin', 'catear', 'long']
TAILS=['fluffy', 'cat']

def make_gacha(out, dur, seed=0, fps=30):
	random.seed(seed)
	os.environ['IMAGEIO_FFMPEG_EXE'] = os.path.abspath(os.path.join(os.getcwd(), 'tools', 'ffmpeg.exe'))
	sk=random.choice(SKINS); hr=random.choice(HAIRS); ey=random.choice(EYES); tp=random.choice(TOPS); bt=random.choice(BOTTOMS); st=random.choice(STYLES); tl=random.choice(TAILS)
	from moviepy.video.VideoClip import VideoClip
	def mk(t):
		img = Image.new('RGB', (W, H), (180,220,255))
		dr = ImageDraw.Draw(img)
		for y in range(0, H//2, 8):
			f = y/(H//2)
			dr.rectangle([0, y, W, y+8], fill=(int(120 + 80 * f), int(180 + 60 * f), int(255 - 20 * f)))
		dr.rectangle([0,H//2,W,H], fill=(120,200,110))
		for _ in range(12):
			fx=random.randint(0,W); fy=random.randint(H//2,H); fr=random.randint(2,5)
			dr.ellipse([fx-fr,fy-fr,fx+fr,fy+fr], fill=random.choice([(255,180,200),(255,220,120),(255,255,255)]))
		bob = math.sin(t * 3)** 14
		draw_char(dr, W//2, H//2 - 140+bob, 175, sk, hr, ey, tp, bt, st, tl)
		return np.array(img)
	clip = VideoClip(mk)
	clip = clip.set_duration(dur) if hasattr(clip,'set_duration') else clip.with_duration(dur)
	clip = clip.set_fps(fps) if hasattr(clip,'set_fps') else clip.with_fps(fps)
	clip.write_videofile(out, fps=fps, codec='libx264', preset='veryfast', audio=False, logger=None)
	return out

