import os, subprocess
FFMPEG = os.path.abspath(os.path.join('tools', 'ffmpeg.exe'))
SRC = 'assets/music'
DST = 'assets/music_clips'
os.makedirs(DST, exist_ok=True)
# cat 20s tai cac vi tri 30, 90, 180, 300 giay
positions = [30, 90, 180, 300]
files = [f for f in os.listdir(SRC) if f.endswith('.webm')]
print('files:', len(files))
for fi, fn in enumerate(files):
	src = os.path.join(SRC, fn)
	for pi, pos in enumerate(positions):
		out = os.path.join(DST, 'clip_%d_%d.mp3' % (fi, pi))
		cmd = [FFMPEG, '-y', '-ss', str(pos), '-t', '20', '-i', src, '-vn', '-acodec', 'libmp3lame', '-ab', '192k', out]
		r = subprocess.run(cmd, capture_output=True)
		ok = os.path.exists(out) and os.path.getsize(out) > 1000
		print(fn, 'pos', pos, '->', ok, os.path.getsize(out) if os.path.exists(out) else 0)