# build_pika_mv2.py - fix cut cuoi + caption dep font Black vien vang
import os, sys, math, subprocess
sys.stdout.reconfigure(encoding='utf-8', errors='replace')
sys.path.insert(0, os.getcwd())
from PIL import Image, ImageEnhance
from ops import voice_synth as VS
from ops import voice_master as VM
FFMPEG = os.path.abspath(os.path.join('tools', 'ffmpeg.exe'))
BW, BH = 720, 1280
FONT = 'tools/font_black.ttf'
# 4 doan voice + caption tuong ung
PARTS = [
	'Pikachu có thực sự là chuột?',
	'Đây là bí mật ít ai biết!',
	'Pikachu dựa trên sóc chuột Nhật Bản!',
	'Đôi má đỏ tích điện hàng nghìn volt!'
]
# Tao voice full (khong cat)
VO = os.path.abspath('output/pika_vo2.mp3')
VS.synth_parts(PARTS, VO, voice='female_north', preset='cute', gap=0.35)
VO_DUR = VM.duration(VO)
print('voice dur:', VO_DUR)
# Chia deu thoi luong cho 4 doan (uoc luong theo do dai text)
total_chars = sum(len(p) for p in PARTS)
segs = []
acc = 0.0
for p in PARTS:
	d = VO_DUR * (len(p) / total_chars)
	segs.append((acc, acc + d))
	acc += d
# Them 0.4s cuoi de cau ket thuc tu nhien
DUR = VO_DUR + 0.5
print('total dur:', DUR)
def fit(im, w, h):
	iw, ih = im.size
	s = max(w / iw, h / ih)
	nw, nh = int(iw * s), int(ih * s)
	im2 = im.resize((nw, nh), Image.LANCZOS)
	x0 = (nw - w) // 2
	y0 = (nh - h) // 2
	return im2.crop((x0, y0, x0 + w, y0 + h))
imgs = ['output/ai_anime/pika' + str(i) + '.jpg' for i in range(6)]
fps = 8
n = int(DUR * fps)
n_img = len(imgs)
seg = DUR / n_img
covers = [fit(Image.open(p).convert('RGB'), BW, BH) for p in imgs]
tmp = 'output/_pika_frames2'
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
# Caption: tao file text + drawtext voi fade in/out
cap_tmp = 'output/_pika_caps'
os.makedirs(cap_tmp, exist_ok=True)
dts = []
for k, (a, b) in enumerate(segs):
	fp = os.path.join(cap_tmp, 'c%d.txt' % k)
	# word wrap ~20 ky tu
	txt = PARTS[k]
	words = txt.split()
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
	# enable + fade alpha: 0.25s in, 0.25s out
	a2 = a + 0.25; b2 = b - 0.25
	en = 'between(t,' + str(round(a, 2)) + ',' + str(round(b, 2)) + ')'
	# alpha fade: dung alpha expression
	al = 'if(lt(t,' + str(round(a + 0.25, 2)) + '),(t-' + str(round(a, 2)) + ')/0.25,if(gt(t,' + str(round(b - 0.25, 2)) + '),(' + str(round(b, 2)) + '-t)/0.25,1))'
	ff = FONT.replace(chr(92), chr(47))
	tf = fp.replace(chr(92), chr(47))
	qt = chr(39)
	s = 'drawtext=fontfile=' + ff + ':textfile=' + tf
	s += ':enable=' + qt + en + qt
	s += ':alpha=' + qt + al + qt
	s += ':fontsize=58:fontcolor=0xFFEB3B:borderw=5:bordercolor=0x1a1a1a:shadowx=3:shadowy=3:shadowcolor=0x000000@0.8:line_spacing=10'
	s += ':x=(w-text_w)/2:y=h-360'
	dts.append(s)
vf = ','.join(dts)
pat = os.path.join(tmp, 'f%04d.png')
silent = 'output/pika_silent2.mp4'
cmd1 = [FFMPEG, '-y', '-framerate', str(fps), '-i', pat, '-vf', vf, '-c:v', 'libx264', '-pix_fmt', 'yuv420p', '-preset', 'ultrafast', '-crf', '21', silent]
r1 = subprocess.run(cmd1, capture_output=True, text=True)
print('cap rc:', r1.returncode)
if r1.returncode != 0:
	print(r1.stderr[-500:])
print('silent:', os.path.getsize(silent) if os.path.exists(silent) else 0)
music = os.path.abspath('assets/music_clips/clip_1_0.mp3')
final = os.path.abspath('output/Mialinhcute_anime_pika2.mp4')
cmd2 = [FFMPEG, '-y', '-i', silent, '-i', VO, '-i', music, '-filter_complex', '[1:a]volume=1.6[a1];[2:a]volume=0.22[a2];[a1][a2]amix=inputs=2:duration=first[aout]', '-map', '0:v', '-map', '[aout]', '-c:v', 'copy', '-c:a', 'aac', '-b:a', '192k', '-shortest', final]
r2 = subprocess.run(cmd2, capture_output=True, text=True)
print('mux rc:', r2.returncode)
print('final:', os.path.getsize(final) if os.path.exists(final) else 0)