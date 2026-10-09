# -- coding: utf-8 --
# modules/render/stock_fallback.py v1.0.0
# Fallback stock video: Pixabay + Coverr khi Pexels het/hong.
import os, sys, json, urllib.request, urllib.parse, time
U = chr(95)
FKEY = U + U + 'file' + U + U
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(globals()[FKEY]))))
sys.path.insert(0, ROOT)
CACHE = os.path.join(ROOT, 'library', 'stock_cache')
os.makedirs(CACHE, exist_ok=True)
UA = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36'

MODULE = {
	'name': 'render.stock_fallback',
	'version': '1.0.0',
	'interface': 'fallback_for_topic(query, n, need) -> list',
	'deps': []
}

def log(m):
	try:
		print('[stock] ' + str(m), flush=True)
	except Exception:
		pass

def env_key(name):
	env = os.path.join(ROOT, '.env')
	if not os.path.exists(env):
		return ''
	for line in open(env, encoding='utf-8'):
		if line.startswith(name):
			return line.split('=', 1)[1].strip()
	return ''

def _get(url, headers, timeout=20):
	req = urllib.request.Request(url, headers=headers)
	with urllib.request.urlopen(req, timeout=timeout) as r:
		return r.read()

def pixabay_search(query, n=5):
	key = env_key('PIXABAY_API_KEY')
	if not key:
		return []
	params = {'key': key, 'q': query, 'per_page': n + n + n, 'video_type': 'film', 'safesearch': 'true'}
	url = 'https://pixabay.com/api/videos/?' + urllib.parse.urlencode(params)
	try:
		data = json.loads(_get(url, {'User-Agent': UA}).decode())
	except Exception:
		return []
	out = []
	for h in data.get('hits', []):
		v = h.get('videos', {})
		best = v.get('large') or v.get('medium') or v.get('small')
		if not best:
			continue
		link = best.get('url')
		if not link:
			continue
		out.append({'id': 'pix' + str(h.get('id')), 'url': link, 'dur': h.get('duration', 0), 'w': best.get('width'), 'h': best.get('height')})
		if len(out) >= n:
			break
	return out

def coverr_search(query, n=5):
	key = env_key('COVERR_API_KEY')
	if not key:
		return []
	url = 'https://api.coverr.co/videos?' + urllib.parse.urlencode({'query': query, 'page_size': n + n + n})
	headers = {'Authorization': 'Bearer ' + key, 'User-Agent': UA}
	try:
		data = json.loads(_get(url, headers).decode())
	except Exception:
		return []
	out = []
	items = data.get('hits', data.get('videos', []))
	for h in items:
		urls = h.get('urls', {}) or {}
		link = urls.get('mp4') or urls.get('mp4_download') or h.get('download_link')
		if not link:
			continue
		out.append({'id': 'cov' + str(h.get('id')), 'url': link, 'dur': h.get('duration', 0)})
		if len(out) >= n:
			break
	return out

def download(video_info, prefix='stock'):
	vid = str(video_info.get('id'))
	out = os.path.join(CACHE, prefix + vid + '.mp4')
	if os.path.exists(out) and os.path.getsize(out) > 10000:
		return out
	try:
		data = _get(video_info['url'], {'User-Agent': UA}, timeout=60)
		if len(data) > 10000:
			open(out, 'wb').write(data)
			return out
	except Exception:
		pass
	return None

def fallback_for_topic(query, n=5, need=2):
	paths = []
	sources = (('pixabay', pixabay_search, 'pix'), ('coverr', coverr_search, 'cov'))
	for name, fn, prefix in sources:
		if len(paths) >= need:
			break
		try:
			vids = fn(query, n + n)
		except Exception:
			vids = []
		log(name + ': ' + str(len(vids)) + ' ket qua')
		for v in vids:
			if len(paths) >= need:
				break
			p = download(v, prefix)
			if p:
				paths.append(p)
	return paths

def health():
	return {'pixabay': bool(env_key('PIXABAY_API_KEY')), 'coverr': bool(env_key('COVERR_API_KEY'))}

