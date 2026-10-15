# tool: ffmpeg
# -- coding: utf-8 --
import os, sys, subprocess, json, re
from operator import mul
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(globals()['__file__']))))
FFMPEG = os.path.join(ROOT, 'tools', 'ffmpeg.exe')

def dur(p):
	r = subprocess.run([FFMPEG, '-i', p, '-hide_banner'], capture_output=True, text=True, creationflags=0x08000000)
	m = re.search('Duration: ([0-9]+):([0-9]+):([0-9.]+)', r.stderr)
	if not m:
		return 0.0
	return mul(int(m.group(1)), 3600) + mul(int(m.group(2)), 60) + float(m.group(3))

def boost(src, out, start=0.8, stop=2.5):
	vf = 'tpad=start_duration=' + str(start) + ':start_mode=add:color=black:stop_duration=' + str(stop) + ':stop_mode=clone'
	cmd = [FFMPEG, '-y', '-i', src, '-vf', vf, '-c:v', 'libx264', '-preset', 'veryfast', '-pix_fmt', 'yuv420p', '-c:a', 'copy', out]
	r = subprocess.run(cmd, capture_output=True, creationflags=0x08000000)
	return {'ok': r.returncode == 0 and os.path.exists(out), 'err': (r.stderr[-250:] if r.returncode != 0 else '')}

if __name__ == '__main__':
	src = sys.argv[1]
	out = sys.argv[2]
	print(json.dumps(boost(src, out), indent=2))
