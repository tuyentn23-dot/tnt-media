from ops import gacha_sprite as _GS
# gacha_maker.py - ve nhan vat gacha CHI TIET (tab)
import os, math, random
import numpy as np
from PIL import Image, ImageDraw, ImageFont
ROOT = os.getcwd()
W, H = 720, 1280

def _shade(c, f):
	return tuple(max(0,min(255,int(x * f))) for x in c)

def _eyes(dr, cx, cy, r, eye, expr):
	ew = int(r * 0.34)
	eh = int(r * 0.44)
	for s in (-1, 1):
		ex = cx + s * int(r * 0.42)
		# long trang oval
		dr.ellipse([ex-ew, cy-eh, ex+ew, cy+eh], fill=(255,255,255))
		# vien tren dam
		dr.arc([ex-ew, cy-eh, ex+ew, cy+eh], 190, 350, fill=(50,40,50), width=5)
		# iris
		iw = int(ew * 0.85); ih = int(eh * 0.85)
		dr.ellipse([ex-iw, cy-ih, ex+iw, cy+ih], fill=eye)
		# iris toi duoi
		dcol = tuple(max(0,int(x * 0.5)) for x in eye)
		dr.ellipse([ex-iw, cy, ex+iw, cy+ih], fill=dcol)
		# dong tu
		pr = int(iw * 0.42)
		dr.ellipse([ex-pr, cy-pr, ex+pr, cy+pr], fill=(25,20,35))
		hr1 = int(iw * 0.4)
		dr.ellipse([ex-iw, cy-ih, ex-iw+hr1*2, cy-ih+hr1*2], fill=(255,255,255))
		dr.ellipse([ex-iw, cy-ih, ex-iw+hr1*2, cy-ih+hr1*2], fill=(255,255,255))
		# highlight nho (duoi phai)
		hr2 = int(iw * 0.22)
		dr.ellipse([ex+iw-hr2*2, cy+ih-hr2*2, ex+iw, cy+ih], fill=(255,255,255))
	# long may
	for s in (-1, 1):
		ex = cx + s * int(r * 0.42)
		dr.arc([ex-ew, cy-eh-int(r * 0.3), ex+ew, cy-eh+int(r * 0.1)], 200, 340, fill=(60,45,55), width=5)
def _hair(dr, cx, cy, r, hair, style):
	h2 = _shade(hair, 0.7)
	if style == 'twin':
		dr.ellipse([cx-r * 1.3, cy-r * 1.2, cx-r * 0.5, cy+r * 0.5], fill=hair)
		dr.ellipse([cx+r * 0.5, cy-r * 1.2, cx+r * 1.3, cy+r * 0.5], fill=hair)
	dr.pieslice([cx-r * 1.1, cy-r * 1.2, cx+r * 1.1, cy+r * 0.7], 180, 360, fill=hair)
	dr.pieslice([cx-r * 0.95, cy-r * 1.0, cx+r * 0.95, cy+r * 0.2], 200, 340, fill=h2)
	if style == 'long':
		dr.ellipse([cx-r * 1.4, cy-r * 0.8, cx-r * 0.7, cy+r * 2.2], fill=hair)
		dr.ellipse([cx+r * 0.7, cy-r * 0.8, cx+r * 1.4, cy+r * 2.2], fill=hair)
	return dr


def _acc(dr, cx, cy, r, acc):
	if acc == 'catear':
		for s in (-1,1):
			ex = cx + math.sin(r * 0.6)
			dr.polygon([(ex, cy-r * 1.0),(ex-math.sin(r * 0.35), cy-r * 1.5),(ex+math.sin(r * 0.1), cy-r * 1.4)], fill=(60,50,60))
	elif acc == 'ribbon':
		dr.polygon([(cx-r * 0.9, cy-r * 0.9),(cx-r * 0.5, cy-r * 1.2),(cx-r * 0.5, cy-r * 0.6)], fill=(255,80,120))
		dr.polygon([(cx-r * 0.5, cy-r * 0.9),(cx-r * 0.1, cy-r * 1.2),(cx-r * 0.1, cy-r*0.6)], fill=(255,80,120))
	return dr

def draw_char(dr, cx, cy, r, mo, hair, skin, eye, shirt, style, acc, expr):
	# than + vai
	dr.ellipse([cx-r * 1.5, cy+r * 1.1, cx+r * 1.5, cy+r * 3.2], fill=shirt)
	dr.ellipse([cx-r * 0.5, cy+r * 1.0, cx+r * 0.5, cy+r * 1.5], fill=skin)
	# dau
	dr.ellipse([cx-r, cy-r, cx+r, cy+r], fill=skin)
	# tai
	_acc(dr, cx, cy, r, acc)
	# toc
	_hair(dr, cx, cy, r, hair, style)
	# mat
	_eyes(dr, cx, cy, r, eye, expr)
	# mieng
	mw = int(r * 0.3); mh = int(r * 0.35 * mo) + 2
	dr.ellipse([cx-mw, cy+r * 0.45-mh, cx+mw, cy+r * 0.45+mh], fill=(200,80,90))
	# blush
	dr.ellipse([cx-r * 0.8, cy+r * 0.2, cx-r * 0.5, cy+r * 0.42], fill=(255,180,190))
	dr.ellipse([cx+r * 0.5, cy+r * 0.2, cx+r * 0.8, cy+r * 0.42], fill=(255,180,190))
	return dr

HAIRS = [(255,150,190),(90,50,140),(210,70,110),(50,120,190),(230,150,50),(70,170,90),(60,60,80),(200,200,220),(120,80,60)]
SKINS = [(255,224,196),(245,210,180),(220,180,150)]
EYES = [(80,120,220),(150,60,180),(60,160,120),(200,60,60),(90,90,160)]
SHIRTS = [(80,120,220),(200,80,120),(60,160,120),(230,180,60),(120,80,180)]
STYLES = ['twin', 'long', 'short']
ACCS = ['catear', 'ribbon', 'none']

def make_gacha(out, dur, seed=0, fps=30, expr='happy'):
	random.seed(seed)
	os.environ['IMAGEIO_FFMPEG_EXE'] = os.path.abspath(os.path.join(ROOT, 'tools', 'ffmpeg.exe'))
	hair = random.choice(HAIRS); skin = random.choice(SKINS); eye = random.choice(EYES)
	shirt = random.choice(SHIRTS); style = random.choice(STYLES); acc = random.choice(ACCS)
	from moviepy.video.VideoClip import VideoClip
	def mk(t):
		img = Image.new('RGB', (W, H), (35,25,60))
		dr = ImageDraw.Draw(img)
		for y in range(0, H, 8):
			f = y / H
			dr.rectangle([0, y, W, y+8], fill=(int(40 + 30 * (1 - f)), int(25 + 40 * (1 - f)), int(70 + 50 * (1 - f))))
		for _ in range(25):
			x = random.randint(0,W); y = random.randint(0,H); rr = random.randint(1,3)
			dr.ellipse([x-rr,y-rr,x+rr,y+rr], fill=(255,255,255))
		bob = math.sin(t * 3) * 14
		mo = 0.5 + 0.5 * abs(math.sin(t * 11))
		draw_char(dr, W//2, H//2 - 120 + bob, 210, mo, hair, skin, eye, shirt, style, acc, expr)
		return np.array(img)
	clip = VideoClip(mk)
	clip = clip.set_duration(dur) if hasattr(clip, 'set_duration') else clip.with_duration(dur)
	clip = clip.set_fps(fps) if hasattr(clip, 'set_fps') else clip.with_fps(fps)
	clip.write_videofile(out, fps=fps, codec='libx264', preset='veryfast', audio=False, logger=None)
	return out
def make_gacha_story(out, dur, seed=0, fps=30):
	random.seed(seed)
	os.environ['IMAGEIO_FFMPEG_EXE'] = os.path.abspath(os.path.join(ROOT, 'tools', 'ffmpeg.exe'))
	h1=random.choice(HAIRS); s1=random.choice(SKINS); e1=random.choice(EYES); sh1=random.choice(SHIRTS); st1=random.choice(STYLES); ac1=random.choice(ACCS)
	h2=random.choice(HAIRS); s2=random.choice(SKINS); e2=random.choice(EYES); sh2=random.choice(SHIRTS); st2=random.choice(STYLES); ac2=random.choice(ACCS)
	from moviepy.video.VideoClip import VideoClip
	def mk(t):
		img = Image.new('RGB', (W, H), (35,25,60))
		dr = ImageDraw.Draw(img)
		for y in range(0, H, 8):
			f = y / H
			dr.rectangle([0, y, W, y+8], fill=(int(40 + 30 * (1 - f)), int(25 + 40 * (1 - f)), int(70 + 50 * (1 - f))))
		for _ in range(25):
			x = random.randint(0,W); yy = random.randint(0,H); rr = random.randint(1,3)
			dr.ellipse([x-rr,yy-rr,x+rr,yy+rr], fill=(255,255,255))
		bob = math.sin(t * 3) * 14
		mo = 0.5 + 0.5 * abs(math.sin(t * 11))
		expr1 = 'happy' if int(t) % 6 < 3 else 'sad'
		expr2 = 'sad' if int(t) % 6 < 3 else 'happy'
		draw_char(dr, W//2 - 150, H//2 - 150 + bob, 150, mo, h1, s1, e1, sh1, st1, ac1, expr1)
		draw_char(dr, W//2 + 150, H//2 + 50 - bob, 150, mo, h2, s2, e2, sh2, st2, ac2, expr2)
		return np.array(img)
	clip = VideoClip(mk)
	clip = clip.set_duration(dur) if hasattr(clip, 'set_duration') else clip.with_duration(dur)
	clip = clip.set_fps(fps) if hasattr(clip, 'set_fps') else clip.with_fps(fps)
	clip.write_videofile(out, fps=fps, codec='libx264', preset='veryfast', audio=False, logger=None)
	return out

