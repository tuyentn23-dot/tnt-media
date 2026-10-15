# ops/video_reader.py - Doc video bang vision model (moondream) + ffmpeg
# Extract frames -> vision analyze -> tra ve: noi dung, co chu, do sang, scene type
import os, sys, base64, json, subprocess, tempfile, shutil, re
U = chr(95)
FKEY = U + U + 'file' + U + U
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(globals()[FKEY])))
sys.path.insert(0, ROOT)
FFMPEG = os.path.join(ROOT, 'tools', 'ffmpeg.exe')
OLLAMA = 'http://127.0.0.1:11434'
VISION_MODEL = 'moondream:latest'


def log(m):
	try:
		print('[video_reader] ' + str(m), flush=True)
	except Exception:
		pass


def probe_dur(path):
	try:
		r = subprocess.run([FFMPEG, '-i', path, '-hide_banner'], capture_output=True, text=True, timeout=30, creationflags=0x08000000)
		m = re.search('Duration: (\d+):(\d+):(\d+\.\d+)', r.stderr)
		if m:
			return int(m.group(1)) * 3600 + int(m.group(2)) * 60 + float(m.group(3))
	except Exception:
		pass
	return 0.0


def extract_frames(path, n=8, tmpdir=None):
	# Trich n frames deu nhau
	dur = probe_dur(path)
	if dur <= 0:
		return []
	tmp = tmpdir or tempfile.mkdtemp(prefix='vframes')
	frames = []
	for i in range(n):
		t = dur * (i + 0.5) / n
		fp = os.path.join(tmp, 'f' + str(i).zfill(2) + '.jpg')
		r = subprocess.run([FFMPEG, '-y', '-ss', str(round(t, 2)), '-i', path, '-frames:v', '1', '-q:v', '3', fp], capture_output=True, creationflags=0x08000000)
		if os.path.exists(fp) and os.path.getsize(fp) > 0:
			frames.append({'idx': i, 't': round(t, 2), 'path': fp})
	return frames


def _brightness(path):
	# Tinh do sang trung binh = file size cua JPEG nho -> uoc luong
	try:
		import numpy as np
		from PIL import Image
		img = Image.open(path).convert('L')
		arr = np.asarray(img, dtype=np.float32)
		return float(arr.mean()), float(arr.std())
	except Exception:
		return -1.0, -1.0


def _encode_b64(path):
	with open(path, 'rb') as f:
		return base64.b64encode(f.read()).decode('ascii')


def vision_ask(img_path, prompt='Describe what is in this image in 1 short English sentence. Then say if there is any text: reply format NOSCENE: <desc> | TEXT: yes/no', timeout=60):
	try:
		import urllib.request
		b64 = _encode_b64(img_path)
		body = json.dumps({'model': VISION_MODEL, 'prompt': prompt, 'images': [b64], 'stream': False, 'options': {'temperature': 0.1, 'num_predict': 80}}).encode('utf-8')
		req = urllib.request.Request(OLLAMA + '/api/generate', data=body, headers={'Content-Type': 'application/json'}, method='POST')
		r = urllib.request.urlopen(req, timeout=timeout)
		d = json.loads(r.read())
		return (d.get('response') or '').strip()
	except Exception as e:
		return 'VISION_ERR: ' + str(e)[:120]


def read_video(path, n_frames=6, use_vision=True, vision_timeout=60):
	# Doc video: trich frames + brightness + vision analyze
	if not os.path.exists(path):
		return {'ok': False, 'error': 'file not found'}
	dur = probe_dur(path)
	tmp = tempfile.mkdtemp(prefix='vread')
	result = {'ok': True, 'path': path, 'duration': round(dur, 2), 'frames': [], 'black_frames': 0, 'avg_brightness': 0.0}
	try:
		frames = extract_frames(path, n=n_frames, tmpdir=tmp)
		if not frames:
			return {'ok': False, 'error': 'no frames extracted'}
		brights = []
		black_idx = []
		for f in frames:
			br, sd = _brightness(f['path'])
			f['brightness'] = round(br, 1)
			f['brightness_std'] = round(sd, 1)
			f['is_black'] = br >= 0 and br < 15
			f['is_near_black'] = br >= 0 and br < 25
			if f['is_black']:
				black_idx.append(f['idx'])
			if br >= 0:
				brights.append(br)
			if use_vision:
				f['vision'] = vision_ask(f['path'], timeout=vision_timeout)
			result['frames'].append(f)
		result['black_frames'] = len(black_idx)
		result['black_indices'] = black_idx
		result['avg_brightness'] = round(sum(brights) / len(brights), 1) if brights else 0.0
		# Chan doan
		issues = []
		last_frames_black = [i for i in black_idx if i >= len(frames) - 2]
		if last_frames_black:
			issues.append('CUOI VIDEO BI DEN (frames ' + str(last_frames_black) + ') - co the booster tpad sai')
		if result['avg_brightness'] < 25:
			issues.append('VIDEO QUA TOI (avg brightness ' + str(result['avg_brightness']) + ')')
		result['issues'] = issues
	finally:
		try:
			shutil.rmtree(tmp, ignore_errors=True)
		except Exception:
			pass
	return result


if __name__ == '__main__':
	import io
	sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='ascii', errors='replace')
	p = sys.argv[1] if len(sys.argv) > 1 else 'output/TEST_express_boost.mp4'
	r = read_video(p, n_frames=6)
	print(json.dumps(r, ensure_ascii=False, indent=2))
