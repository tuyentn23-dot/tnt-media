# gacha_anime_test.py - test render nhanh voi skeleton + hair bezier
import sys, math, random, os
sys.path.insert(0, 'ops')
import importlib
sk = importlib.import_module('gacha_anime')
p2 = importlib.import_module('gacha_anime_p2')
p3 = importlib.import_module('gacha_anime_p3')
from PIL import Image, ImageDraw, ImageFilter

S = 4
W, H = 720 * S, 1280 * S

def render_test(t=0.0, seed=0):
	random.seed(seed)
	img = Image.new('RGB', (W, H), (200, 225, 255))
	dr = ImageDraw.Draw(img)
	# background gradient
	for y in range(0, int(H * 0.65), 6):
		f = y / (H * 0.65)
		dr.rectangle([0, y, W, y + 6], fill=(int(140 + 60 * f), int(190 + 50 * f), int(255 - 30 * f)))
	dr.rectangle([0, int(H * 0.65), W, H], fill=(130, 195, 120))
	# nhan vat
	cx = W // 2
	cy = int(H * 0.30)
	r = int(230 * S)
	j = sk.skeleton(cx, cy, r, t)
	hair = (255, 130, 180)
	skin = (255, 226, 205)
	hair_dark = (210, 95, 150)
	# ---- toc back layer ----
	hpaths = p3.hair_paths(cx, cy, r, 'long')
	for name, pts in hpaths:
		if name == 'back':
			p2.draw_path(dr, pts, int(70 * S), hair_dark, 30)
	# ---- than (ao) ----
	sh_l = j['shoulder_l']
	sh_r = j['shoulder_r']
	hip_l = j['hip_l']
	hip_r = j['hip_r']
	dr.polygon([sh_l, sh_r, hip_r, hip_l], fill=(50, 50, 75))
	# ---- tay (path theo khuuyu) ----
	for side in ('l', 'r'):
		sh = j['shoulder_' + side]
		el = j['elbow_' + side]
		wr = j['wrist_' + side]
		p2.draw_path(dr, [sh, el, wr], int(28 * S), skin, 8)
	# ---- chan ----
	for side in ('l', 'r'):
		hp = j['hip_' + side]
		kn = j['knee_' + side]
		an = j['ankle_' + side]
		p2.draw_path(dr, [hp, kn, an], int(32 * S), skin, 8)
	# ---- dau ----
	head = j['head']
	dr.ellipse([head[0] - r * 0.78, head[1] - r * 0.9, head[0] + r * 0.78, head[1] + r * 0.95], fill=skin)
	# mat
	eye_y = head[1] + r * 0.05
	dr.ellipse([head[0] - r * 0.42, eye_y - r * 0.15, head[0] - r * 0.1, eye_y + r * 0.25], fill=(255, 255, 255))
	dr.ellipse([head[0] + r * 0.1, eye_y - r * 0.15, head[0] + r * 0.42, eye_y + r * 0.25], fill=(255, 255, 255))
	dr.ellipse([head[0] - r * 0.35, eye_y - r * 0.08, head[0] - r * 0.15, eye_y + r * 0.18], fill=(120, 90, 220))
	dr.ellipse([head[0] + r * 0.15, eye_y - r * 0.08, head[0] + r * 0.35, eye_y + r * 0.18], fill=(120, 90, 220))
	dr.ellipse([head[0] - r * 0.3, eye_y - r * 0.05, head[0] - r * 0.2, eye_y + r * 0.08], fill=(255, 255, 255))
	dr.ellipse([head[0] + r * 0.2, eye_y - r * 0.05, head[0] + r * 0.3, eye_y + r * 0.08], fill=(255, 255, 255))
	# mieng
	dr.ellipse([head[0] - r * 0.1, eye_y + r * 0.45, head[0] + r * 0.1, eye_y + r * 0.6], fill=(220, 80, 110))
	# ---- toc front layer ----
	for name, pts in hpaths:
		if __name__ == '__main__':
			p2.draw_path(dr, pts, int(85 * S), hair, 30)
	for name, pts in hpaths:
		if name == 'fringe':
			p2.draw_path(dr, pts, int(55 * S), hair, 20)
	# blur nhe cho anti-alias mem
	img = img.filter(ImageFilter.GaussianBlur(0.8))
	return img.resize((720, 1280), Image.LANCZOS)

if __name__ == '__main__':
	outdir = 'output/CHECK'
	os.makedirs(outdir, exist_ok=True)
	for i, t in enumerate([0.0, 1.5, 3.0]):
		im = render_test(t, seed=7)
		p = os.path.join(outdir, 'anime_test_%d.png' % i)
		im.save(p)
		print('saved', p)
	print('DONE')
