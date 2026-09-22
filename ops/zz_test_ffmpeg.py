import os, subprocess
os.chdir(os.getcwd()) # workspace root
FFMPEG = os.path.abspath(os.path.join('tools', 'ffmpeg.exe'))
# dung relative path (khong co D:)
pat = 'output/_pika_frames2/f%04d.png'
out = 'output/zz_test_cap.mp4'
font = 'tools/font_black.ttf'
cap = 'output/_pika_caps/c0.txt'
qt = chr(39)
vf = 'drawtext=fontfile=' + font + ':textfile=' + cap + ':enable=' + qt + 'between(t,0,3)' + qt + ':fontsize=58:fontcolor=0xFFEB3B:borderw=5:bordercolor=0x1a1a1a:x=(w-text_w)/2:y=h-360'
cmd = [FFMPEG, '-y', '-framerate', '8', '-i', pat, '-vf', vf, '-c:v', 'libx264', '-pix_fmt', 'yuv420p', '-preset', 'ultrafast', '-crf', '23', out]
r = subprocess.run(cmd, capture_output=True, text=True)
print('rc:', r.returncode)
if r.returncode != 0:
	print(r.stderr[-500:])
else:
	print('ok:', os.path.getsize(out))