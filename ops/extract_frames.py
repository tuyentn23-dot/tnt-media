import os, subprocess
FF = os.path.abspath(os.path.join('tools', 'ffmpeg.exe'))
vid = os.path.abspath('output/Mialinhcute_gacha_crush.mp4')
for t in [1, 2, 3, 4, 5, 6]:
	out = 'output/fr_%d.png' % t
	subprocess.run([FF, '-y', '-ss', str(t), '-i', vid, '-vframes', '1', out], capture_output=True)
	print(t, os.path.getsize(out) if os.path.exists(out) else 0)