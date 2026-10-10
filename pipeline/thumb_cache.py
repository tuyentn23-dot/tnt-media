# pipeline/thumb_cache.py - Cache thumbnail cho video
import os, sys, subprocess, hashlib
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT not in sys.path:
	sys.path.insert(0, ROOT)

CACHE_DIR = os.path.join(ROOT, 'state', 'thumb')
FFMPEG = os.path.join(ROOT, 'tools', 'ffmpeg.exe')


def get_thumb(video_path, force=False):
	'''Tra ve duong dan thumbnail. Tu dong tao neu chua co.'''
	if not video_path or not os.path.exists(video_path):
		return None
	os.makedirs(CACHE_DIR, exist_ok=True)
	h = hashlib.md5((video_path + str(os.path.getmtime(video_path))).encode()).hexdigest()[:16]
	out = os.path.join(CACHE_DIR, h + '.jpg')
	if os.path.exists(out) and not force:
		return out
	if not os.path.exists(FFMPEG):
		return None
	try:
		r = subprocess.run([
			FFMPEG, '-y', '-ss', '0.5', '-i', video_path,
			'-frames:v', '1', '-vf', 'scale=200:-1', '-q:v', '4', out
		], capture_output=True, timeout=15, creationflags=0x08000000)
		if os.path.exists(out):
			return out
	except Exception:
		pass
	return None
