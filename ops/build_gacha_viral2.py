# build_gacha_viral2.py - video gacha girl viral (content ngan gon, caption dep)
import os, sys, math, subprocess
sys.stdout.reconfigure(encoding='utf-8', errors='replace')
sys.path.insert(0, os.getcwd())
from PIL import Image, ImageEnhance
from ops import voice_synth as VS
from ops import voice_master as VM
FFMPEG = os.path.abspath(os.path.join('tools', 'ffmpeg.exe'))
BW, BH = 720, 1280
FONT = 'tools/font_black.ttf'
PARTS = [
	'POV: Co gai meo hong de thuong nhat truong!',
	'Ai cung nguong mo ngoai hinh cua co ay!',
	'Nhung khong ai biet bi mat dang sau!',
	'Co ay khoc mot minh moi dem!',
	'Va roi co ay quyet dinh yeu ban than!',
]
VO = os.path.abspath('output/gacha_vo2.mp3')
VS.synth_parts(PARTS, VO, voice='female_north', preset='cute', gap=0.3)
VO_DUR = VM.duration(VO)
print('voice dur:', VO_DUR)
DUR = min(VO_DUR + 0.5, 19.5)
print('total dur:', DUR)
total_chars = sum(len(p) for p in PARTS)
segs = []
acc = 0.0
for p in PARTS:
	d = VO_DUR * (len(p) / total_chars)
	segs.append((acc, acc + d))
	acc += d
def fit(im, w, h):
	iw, ih = im.size
	s = max(w / iw, h / ih)
	nw, nh = int(iw * s), int(ih * s)
	im2 = im.resize((nw, nh), Image.LANCZOS)
	x0 = (nw - w) // 2
	y0 = (nh - h) // 2
	return im2.crop((x0, y0, x0 + w, y0 + h))
imgs = ['output/gacha_char/pose' + str(i) + '.jpg' for i in range(6)]
fps = 8
n = int((DUR + 0.5) * fps)
n_img = len(imgs)
seg = DUR / n_img
covers = [fit(Image.open(p).convert('RGB'), BW, BH) for p in imgs]
tmp = 'output/_gacha2_frames'
os.makedirs(tmp, exist_ok=True)
for i in range(n):
	t = i / fps
	idx = min(n_img - 1, int(t / seg))
	local_t = (t % seg) / seg
	zoom = 1.0 + 0.15 * local_t
	base = covers[idx]
	nw, nh = int(BW * zoom), int(BH * zoom)
	im2 = base.resize((nw, nh), Image.LANCZOS)
	px = int(20 * math.sin(t * 2.0))
	py = int(15 * math.cos(t * 1.7))
	x0 = max(0, min(nw - BW, (nw - BW) // 2 + px))
	y0 = max(0, min(nh - BH, (nh - BH) // 2 + py))
	crop = im2.crop((x0, y0, x0 + BW, y0 + BH))
	if local_t > 0.88 and idx < n_img - 1:
		a = (local_t - 0.88) / 0.12
		crop = Image.blend(crop, covers[idx + 1], a)
	if t < 0.2:
		crop = ImageEnhance.Brightness(crop).enhance(0.35)
	elif t < 0.5:
		crop = ImageEnhance.Brightness(crop).enhance(1.5)
	if t > DUR - 0.5:
		k = (DUR - t) / 0.5
		crop = Image.blend(covers[0], crop, k)
	crop.save(os.path.join(tmp, 'f%04d.png' % i))
cap_tmp = 'output/_gacha2_caps'
os.makedirs(cap_tmp, exist_ok=True)
dts = []
for k, (a, b) in enumerate(segs):
	fp = cap_tmp + '/' + ('c%d.txt' % k)
	words = PARTS[k].split()
	lines = []
	cur = ''
	for w in words:
		if len(cur) + len(w) + 1 > 20:
			lines.append(cur)
			cur = w
		else:
			cur = (cur + ' ' + w).strip()
	if cur:
		lines.append(cur)
	open(fp, 'w', encoding='utf-8').write(chr(10).join(lines))
	en = 'between(t,' + str(round(a, 2)) + ',' + str(round(b + 0.1, 2)) + ')'
	qt = chr(39)
	s = 'drawtext=fontfile=' + FONT + ':textfile=' + fp + ':enable=' + qt + en + qt
	s += ':fontsize=56:fontcolor=0xFFFFFF:borderw=6:bordercolor=0xFF1493:shadowx=4:shadowy=4:shadowcolor=0x000000@0.9:line_spacing=12'
	s += ':x=(w-text_w)/2:y=h-380'
	dts.append(s)
vf = ','.join(dts)
pat = os.path.join(tmp, 'f%04d.png')
silent = 'output/gacha2_silent.mp4'
cmd1 = [FFMPEG, '-y', '-framerate', str(fps), '-i', pat, '-vf', vf, '-t', str(DUR), '-c:v', 'libx264', '-pix_fmt', 'yuv420p', '-preset', 'ultrafast', '-crf', '21', silent]
r1 = subprocess.run(cmd1, capture_output=True, text=True)
print('cap rc:', r1.returncode)
if r1.returncode != 0:
	print(r1.stderr[-500:])
music = os.path.abspath('assets/music_clips/clip_2_0.mp3')
final = os.path.abspath('output/Mialinhcute_gacha_viral2.mp4')
cmd2 = [FFMPEG, '-y', '-i', silent, '-i', VO, '-i', music, '-filter_complex', '[1:a]volume=1.6[a1];[2:a]volume=0.2[a2];[a1][a2]amix=inputs=2:duration=first[aout]', '-map', '0:v', '-map', '[aout]', '-t', str(DUR), '-c:v', 'copy', '-c:a', 'aac', '-b:a', '192k', final]
r2 = subprocess.run(cmd2, capture_output=True, text=True)
print('mux rc:', r2.returncode)
if r2.returncode != 0:
	print(r2.stderr[-500:])
print('final:', os.path.getsize(final) if os.path.exists(final) else 0)
