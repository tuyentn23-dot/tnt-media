# -- coding: utf-8 --
# Quality Gate
import os, subprocess, re

def _ff():
	root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
	ff = os.path.join(root, 'tools', 'ffmpeg.exe')
	return ff if os.path.exists(ff) else 'ffmpeg'

def probe(path):
	r = subprocess.run([_ff(), '-i', path, '-hide_banner'], capture_output=True, text=True)
	err = r.stderr
	info = {'dur': 0.0, 'w': 0, 'h': 0, 'has_audio': False, 'size': 0}
	m = re.search('Duration: ([0-9]+):([0-9]+):([0-9.]+)', err)
	if m:
		info['dur'] = int(m.group(1))*3600 + int(m.group(2))*60 + float(m.group(3))
	for line in err.splitlines():
		if 'Video:' in line:
			m2 = re.search('([0-9]{3,4})x([0-9]{3,4})', line)
			if m2:
				info['w'] = int(m2.group(1))
				info['h'] = int(m2.group(2))
		if 'Audio:' in line:
			info['has_audio'] = True
	if os.path.exists(path):
		info['size'] = os.path.getsize(path)
	return info

def evaluate(path, title=''):
	errors = []
	warnings = []
	info = probe(path)
	dur = info['dur']
	w = info['w']
	h = info['h']
	if dur < 5:
		errors.append('too short: ' + str(dur))
	if dur > 180:
		errors.append('too long: ' + str(dur))
	if not info['has_audio']:
		errors.append('no audio')
	if info['size'] < 200000:
		errors.append('file too small')
	if dur < 60:
		if (w, h) != (1080, 1920):
			errors.append('Shorts must be 1080x1920')
	else:
		if (w, h) != (1920, 1080):
			warnings.append('long video not 16:9')
	if title and len(title) > 100:
		errors.append('title too long')
	return {'ok': len(errors) == 0, 'errors': errors, 'warnings': warnings, 'info': info}