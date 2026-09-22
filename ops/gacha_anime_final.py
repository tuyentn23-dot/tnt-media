# gacha_anime_final.py - render anime gacha FULL (skeleton + bezier + parts + video)
import sys, math, random, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import importlib
sk = importlib.import_module('gacha_anime')
p2 = importlib.import_module('gacha_anime_p2')
p3 = importlib.import_module('gacha_anime_p3')
parts = importlib.import_module('gacha_anime_parts')
from PIL import Image, ImageDraw, ImageFilter

S = 4
W, H = 720 * S, 1280 * S

PALETTES = [
	{'hair': (255, 130, 180), 'skin': (255, 226, 205), 'eye': (140, 90, 220), 'top': (50, 50, 75), 'bottom': (255, 140, 190), 'sock': (250, 250, 255)},
	{'hair': (150, 100, 220), 'skin': (250, 218, 195), 'eye': (255, 90, 150), 'top': (40, 40, 60), 'bottom': (180, 120, 220), 'sock': (240, 240, 250)},
	{'hair': (255, 200, 110), 'skin': (255, 228, 210), 'eye': (80, 160, 220), 'top': (60, 45, 80), 'bottom': (255, 180, 120), 'sock': (255, 240, 240)},
]

def shade(c, f):
	return tuple(max(0, min(255, int(v * f))) for v in c)

def draw_bg(dr, t):
	for y in range(0, int(H * 0.62), 6):
		f = y / (H * 0.62)
		dr.rectangle([0, y, W, y + 6], fill=(int(140 + 60 * f), int(190 + 50 * f), int(255 - 30 * f)))
	dr.rectangle([0, int(H * 0.62), W, H], fill=(130, 195, 120))
	# may troi
	random.seed(int(t * 2))
	for _ in range(5):
		mx = random.randint(0, W)
		my = random.randint(50, int(H * 0.4))
		mw = random.randint(80, 200) * S // 2
		dr.ellipse([mx - mw, my - mw // 3, mx + mw, my + mw // 3], fill=(255, 255, 255))


def render_frame(pal, t, seed=0):
	random.seed(seed)
	img = Image.new('RGB', (W, H), (200, 225, 255))
	dr = ImageDraw.Draw(img)
	draw_bg(dr, t)
	cx = W // 2
	cy = int(H * 0.30)
	r = int(230 * S)
	j = sk.skeleton(cx, cy, r, t)
	hair = pal['hair']
	skin = pal['skin']
	hair_dark = shade(hair, 0.82)
	top = pal['top']
	hpaths = p3.hair_paths(cx, cy, r, 'long')
	# back hair
	for name, pts in hpaths:
		if name == 'back':
			p2.draw_path(dr, pts, int(70 * S), hair_dark, 30)
	# than + ao
	sh_l = j['shoulder_l']
	sh_r = j['shoulder_r']
	hip_l = j['hip_l']
	hip_r = j['hip_r']
	dr.polygon([sh_l, sh_r, hip_r, hip_l], fill=top)
	parts.draw_folds(dr, sh_l, sh_r, hip_l, hip_r, top)
	# tay + ban tay + ngon
	for side in ('l', 'r'):
		sh = j['shoulder_' + side]
		el = j['elbow_' + side]
		wr = j['wrist_' + side]
		p2.draw_path(dr, [sh, el, wr], int(28 * S), skin, 8)
		parts.draw_hand(dr, wr, el, r, skin, spread=1.0)
	# chan
	for side in ('l', 'r'):
		hp = j['hip_' + side]
		kn = j['knee_' + side]
		an = j['ankle_' + side]
		p2.draw_path(dr, [hp, kn, an], int(32 * S), skin, 8)
		# giay
		dr.ellipse([an[0] - r * 0.16, an[1] - r * 0.05, an[0] + r * 0.16, an[1] + r * 0.14], fill=(40, 40, 55))
	# dau + mat + mieng
	head = j['head']
	dr.ellipse([head[0] - r * 0.78, head[1] - r * 0.9, head[0] + r * 0.78, head[1] + r * 0.95], fill=skin)
	openness = 1.0
	open_amt = 0.5 + 0.5 * math.sin(t * 6)
	if math.sin(t * 1.3) > 0.96:
		openness = 0.05
	parts.draw_eyes(dr, head, r, pal['eye'], openness, look=math.sin(t * 0.9) * 0.4)
	parts.draw_blush(dr, head, r)
	parts.draw_mouth(dr, head, r, open_amt, smile=math.sin(t * 1.1))
	# front hair
	for name, pts in hpaths:
		if name == 'main':
			p2.draw_path(dr, pts, int(85 * S), hair, 30)
	for name, pts in hpaths:
		if name == 'fringe':
			p2.draw_path(dr, pts, int(55 * S), hair, 20)
	img = img.filter(ImageFilter.GaussianBlur(0.8))
	return img.resize((720, 1280), Image.LANCZOS)


def make_video(out, dur, seed=0, fps=30, pal_idx=0):
	os.environ['IMAGEIO_FFMPEG_EXE'] = os.path.abspath(os.path.join('tools', 'ffmpeg.exe'))
	pal = PALETTES[pal_idx % len(PALETTES)]
	from moviepy.video.VideoClip import VideoClip
	import numpy as np
	def mk(t):
		return np.array(render_frame(pal, t, seed))
	clip = VideoClip(mk)
	clip = clip.set_duration(dur) if hasattr(clip, 'set_duration') else clip.with_duration(dur)
	clip = clip.set_fps(fps) if hasattr(clip, 'set_fps') else clip.with_fps(fps)
	clip.write_videofile(out, fps=fps, codec='libx264', preset='veryfast', audio=False, logger=None)
	return out


if __name__ == '__main__':
	outdir = 'output/CHECK'
	os.makedirs(outdir, exist_ok=True)
	for i, t in enumerate([0.0, 1.5, 3.0, 4.5]):
		for pi in range(3):
			im = render_frame(PALETTES[pi], t, seed=7)
			p = os.path.join(outdir, 'anime_final_%d_%d.png' % (pi, i))
			im.save(p)
	print('rendered 12 frames')
	print('DONE')
