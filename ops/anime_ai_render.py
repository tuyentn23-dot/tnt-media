# anime_ai_render.py - Anime MV tu anh AI (pollinations), Ken Burns + crossfade + hook flash + loop
import os, sys, math, subprocess
sys.stdout.reconfigure(encoding='utf-8', errors='replace')
from PIL import Image, ImageEnhance, ImageFilter
FFMPEG = os.path.abspath(os.path.join('tools', 'ffmpeg.exe'))
BW, BH = 720, 1280
def fit_cover(im, w, h):
	# scale anh de cover w x h, cat center
	iw, ih = im.size
	scale = max(w / iw, h / ih)
	nw, nh = int(iw * scale), int(ih * scale)
	im2 = im.resize((nw, nh), Image.LANCZOS)
	x0 = (nw - w) // 2
	y0 = (nh - h) // 2
	return im2.crop((x0, y0, x0 + w, y0 + h))
def make_mv(images, out, dur=12.0, fps=8):
	n_frames = int(dur * fps)
	n_img = len(images)
	seg = n_frames / n_img
	tmpdir = 'output/_mv_tmp'
	os.makedirs(tmpdir, exist_ok=True)
	# preload + fit cover
	covers = [fit_cover(Image.open(p).convert('RGB'), BW, BH) for p in images]
	for i in range(n_frames):
		t = i / fps
		# tim anh hien tai + anh ke
		idx = min(n_img - 1, int(t / (dur / n_img)))
		next_idx = min(n_img - 1, idx + 1)
		local_t = (t % (dur / n_img)) / (dur / n_img)
		# ken burns zoom 1.0 -> 1.12 tren anh hien tai
		zoom = 1.0 + 0.12 * local_t
		base = covers[idx]
		nw, nh = int(BW * zoom), int(BH * zoom)
		im2 = base.resize((nw, nh), Image.LANCZOS)
		pan_x = int(15 * math.sin(t * 1.5))
		x0 = max(0, min(nw - BW, (nw - BW) // 2 + pan_x))
		y0 = (nh - BH) // 2
		crop = im2.crop((x0, y0, x0 + BW, y0 + BH))
		# crossfade 0.25s cuoi moi doan
		if local_t > 0.85 and idx < n_img - 1:
			alpha = (local_t - 0.85) / 0.15
			nxt = fit_cover(Image.open(images[next_idx]).convert('RGB'), BW, BH)
			crop = Image.blend(crop, nxt, alpha)
		# hook flash 1.5s dau
		if t < 0.25:
			crop = ImageEnhance.Brightness(crop).enhance(0.4)
		elif t < 0.55:
			crop = ImageEnhance.Brightness(crop).enhance(1.5)
		# loop: 0.4s cuoi toi dan ve sang anh dau (loop_gap nho)
		if t > dur - 0.4:
			k = (dur - t) / 0.4
			crop = Image.blend(covers[0], crop, k)
		crop.save(os.path.join(tmpdir, 'f%04d.png' % i))
	pat = os.path.join(tmpdir, 'f%04d.png')
	cmd = [FFMPEG, '-y', '-framerate', str(fps), '-i', pat, '-c:v', 'libx264', '-pix_fmt', 'yuv420p', '-preset', 'ultrafast', '-crf', '21', out]
	r = subprocess.run(cmd, capture_output=True, text=True)
	print('mv rc:', r.returncode, 'size:', os.path.getsize(out) if os.path.exists(out) else 0)
	return out