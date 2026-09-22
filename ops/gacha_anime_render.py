# gacha_anime_render.py v4 - hook flash + loop seamless
import os, sys, math, subprocess
sys.stdout.reconfigure(encoding='utf-8', errors='replace')
sys.path.insert(0, os.path.join(os.getcwd(), 'ops'))
sys.path.insert(0, 'ops')
import importlib
gf = importlib.import_module('gacha_anime_final')
FFMPEG = os.path.abspath(os.path.join('tools', 'ffmpeg.exe'))
from PIL import Image, ImageEnhance
BW, BH = 720, 1280
def render_pal(dur, pal_idx, seed, fps=6):
	n_total = max(2, int(dur * fps))
	tmpdir = 'output/_anim_tmp4'
	os.makedirs(tmpdir, exist_ok=True)
	for i in range(n_total):
		t = i * (dur / n_total)
		im = gf.render_frame(gf.PALETTES[pal_idx % 3], t * 4, seed=seed)
		is_hook = (i < 3)
		is_end = (i >= n_total - 2)
		# hook: frame 0 toi, frame 1 sang manh (flash)
		if i == 0:
			im = ImageEnhance.Brightness(im).enhance(0.35)
		elif i == 1:
			im = ImageEnhance.Brightness(im).enhance(1.6)
		# loop: frame cuoi giong frame 0 (toi)
		if is_end:
			im = ImageEnhance.Brightness(im).enhance(0.35)
		zoom_fast = 1.0 + (0.35 if is_hook else 0.12) * abs(math.sin(t * (5.0 if is_hook else 2.0)))
		nw = int(BW * zoom_fast); nh = int(BH * zoom_fast)
		im2 = im.resize((nw, nh), Image.LANCZOS)
		pan_x = int((40 if is_hook else 15) * math.sin(t * 6.0))
		pan_y = int((30 if is_hook else 12) * math.cos(t * 5.0))
		x0 = max(0, (nw - BW) // 2 + pan_x)
		y0 = max(0, (nh - BH) // 2 + pan_y)
		crop = im2.crop((x0, y0, x0 + BW, y0 + BH))
		crop.save(os.path.join(tmpdir, 'f%04d.png' % i))
	return tmpdir, n_total
def make_anime(out, dur, seed=0, pal_idx=0, fps=6):
	tmpdir, n = render_pal(dur, pal_idx, seed, fps)
	pat = os.path.join(tmpdir, 'f%04d.png')
	cmd = [FFMPEG, '-y', '-framerate', str(fps), '-i', pat, '-c:v', 'libx264', '-pix_fmt', 'yuv420p', '-preset', 'ultrafast', '-crf', '21', out]
	r = subprocess.run(cmd, capture_output=True, text=True)
	print('anim rc:', r.returncode, 'file:', os.path.getsize(out) if os.path.exists(out) else 0)
	return out