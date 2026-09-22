# build_pika_mv.py - video pikachu chuyen dong theo content (voice sync)
import os, sys, math, subprocess
sys.stdout.reconfigure(encoding='utf-8', errors='replace')
sys.path.insert(0, os.getcwd())
from PIL import Image, ImageEnhance
from ops import voice_master as VM
FFMPEG = os.path.abspath(os.path.join('tools', 'ffmpeg.exe'))
BW, BH = 720, 1280
def fit(im, w, h):
	iw, ih = im.size
	s = max(w / iw, h / ih)
	nw, nh = int(iw * s), int(ih * s)
	im2 = im.resize((nw, nh), Image.LANCZOS)
	x0 = (nw - w) // 2
	y0 = (nh - h) // 2
	return im2.crop((x0, y0, x0 + w, y0 + h))
imgs = ['output/ai_anime/pika' + str(i) + '.jpg' for i in range(6)]
vo = os.path.abspath('output/pika_vo.mp3')
dur = min(VM.duration(vo), 19.5)
print('dur:', dur)
fps = 8
n = int(dur * fps)
n_img = len(imgs)
seg = dur / n_img
covers = [fit(Image.open(p).convert('RGB'), BW, BH) for p in imgs]
tmp = 'output/_pika_frames'
os.makedirs(tmp, exist_ok=True)
for i in range(n):
	t = i / fps
	idx = min(n_img - 1, int(t / seg))
	local_t = (t % seg) / seg
	# zoom ken burns
	zoom = 1.0 + 0.15 * local_t
	base = covers[idx]
	nw, nh = int(BW * zoom), int(BH * zoom)
	im2 = base.resize((nw, nh), Image.LANCZOS)
	px = int(20 * math.sin(t * 2.0))
	py = int(15 * math.cos(t * 1.7))
	x0 = max(0, min(nw - BW, (nw - BW) // 2 + px))
	y0 = max(0, min(nh - BH, (nh - BH) // 2 + py))
	crop = im2.crop((x0, y0, x0 + BW, y0 + BH))
	# crossfade cuoi doan
	if local_t > 0.88 and idx < n_img - 1:
		a = (local_t - 0.88) / 0.12
		crop = Image.blend(crop, covers[idx + 1], a)
	# hook flash 1s dau
	if t < 0.2:
		crop = ImageEnhance.Brightness(crop).enhance(0.35)
	elif t < 0.5:
		crop = ImageEnhance.Brightness(crop).enhance(1.5)
	# loop cuoi
	if t > dur - 0.5:
		k = (dur - t) / 0.5
		crop = Image.blend(covers[0], crop, k)
	crop.save(os.path.join(tmp, 'f%04d.png' % i))
pat = os.path.join(tmp, 'f%04d.png')
silent = 'output/pika_silent.mp4'
cmd1 = [FFMPEG, '-y', '-framerate', str(fps), '-i', pat, '-c:v', 'libx264', '-pix_fmt', 'yuv420p', '-preset', 'ultrafast', '-crf', '21', silent]
subprocess.run(cmd1, capture_output=True)
print('silent:', os.path.getsize(silent))
music = os.path.abspath('assets/music_clips/clip_1_0.mp3')
final = os.path.abspath('output/Mialinhcute_anime_pika.mp4')
cmd2 = [FFMPEG, '-y', '-i', silent, '-i', vo, '-i', music, '-filter_complex', '[1:a]volume=1.6[a1];[2:a]volume=0.22[a2];[a1][a2]amix=inputs=2:duration=first[aout]', '-map', '0:v', '-map', '[aout]', '-c:v', 'copy', '-c:a', 'aac', '-b:a', '192k', '-shortest', final]
r = subprocess.run(cmd2, capture_output=True, text=True)
print('rc:', r.returncode)
if r.returncode != 0:
	print(r.stderr[-500:])
print('final:', os.path.getsize(final) if os.path.exists(final) else 0)