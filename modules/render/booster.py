# tool: ffmpeg
# -- coding: utf-8 --
import os, sys, subprocess, json, re
import math
from operator import mul
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(globals()['__file__']))))
FFMPEG = os.path.join(ROOT, 'tools', 'ffmpeg.exe')

def dur(p):
	r = subprocess.run([FFMPEG, '-i', p, '-hide_banner'], capture_output=True, text=True, creationflags=0x08000000)
	m = re.search('Duration: ([0-9]+):([0-9]+):([0-9.]+)', r.stderr)
	if not m:
		return 0.0
	return mul(int(m.group(1)), 3600) + mul(int(m.group(2)), 60) + float(m.group(3))

MODULE = {'name': 'render.booster', 'version': '2.0.0',
	'interface': 'boost(src, out, start=0, stop=0) -> dict', 'deps': ['ffmpeg']}


def boost(src, out, start=0.0, stop=0.0):
	"""Polish the ending without adding black frames to inflate motion metrics.

	Explicit padding clones the real frame and delays audio by the same amount.
	Default processing preserves duration and fades picture/audio for 0.5 seconds.
	"""
	if os.path.normcase(os.path.abspath(src)) == os.path.normcase(os.path.abspath(out)):
		return {'ok': False, 'err': 'source and output must differ'}
	if not all(math.isfinite(v) and v >= 0 for v in (start, stop)):
		return {'ok': False, 'err': 'padding must be finite and nonnegative'}
	try:
		duration = dur(src)
		if duration <= 0:
			return {'ok': False, 'err': 'cannot decode source duration'}
		total = duration + start + stop
		fade = min(0.5, total / 2)
		fade_at = total - fade
		vf = (f'tpad=start_duration={start}:start_mode=clone:stop_duration={stop}:stop_mode=clone,'
		      f'fade=t=out:st={fade_at}:d={fade}')
		af = f'adelay={round(start * 1000)}:all=1,apad,atrim=duration={total},afade=t=out:st={fade_at}:d={fade}'
		cmd = [FFMPEG, '-hide_banner', '-nostdin', '-y', '-threads', '1', '-i', src,
		       '-map', '0:v:0', '-map', '0:a:0?', '-filter_threads', '1', '-vf', vf, '-af', af,
		       '-c:v', 'libx264', '-threads', '1', '-preset', 'veryfast', '-pix_fmt', 'yuv420p',
		       '-c:a', 'aac', '-t', str(total), '-movflags', '+faststart', out]
		r = subprocess.run(cmd, capture_output=True, text=True, errors='replace', timeout=600,
		                   creationflags=getattr(subprocess, 'CREATE_NO_WINDOW', 0))
		ok = r.returncode == 0 and os.path.isfile(out) and os.path.getsize(out) > 0
		return {'ok': ok, 'path': out, 'duration': round(total, 3),
		        'err': r.stderr[-1000:] if not ok else ''}
	except (OSError, subprocess.TimeoutExpired) as exc:
		return {'ok': False, 'err': str(exc)}

if __name__ == '__main__':
	src = sys.argv[1]
	out = sys.argv[2]
	print(json.dumps(boost(src, out), indent=2))
