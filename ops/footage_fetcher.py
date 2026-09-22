# footage_fetcher.py - download fresh footage from Pexels (tab-indent)
import os, sys, json, requests
ROOT = os.getcwd()
LIB = os.path.join(ROOT, 'library')
CACHE = os.path.join(ROOT, 'memory', 'footage_cache.json')

def _key():
	env = os.path.join(ROOT, '.env')
	txt = open(env, encoding='utf-8').read() if os.path.exists(env) else ''
	return next((l.split('=', 1)[1].strip() for l in txt.splitlines() if l.startswith('PEXELS_API_KEY')), '')

def load_cache():
	return json.load(open(CACHE, encoding='utf-8')) if os.path.exists(CACHE) else {'used': []}

def save_cache(c):
	json.dump(c, open(CACHE, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)

def search(query, per_page=15, orientation='portrait'):
	k = _key()
	url = 'https://api.pexels.com/videos/search'
	params = {'query': query, 'per_page': per_page, 'orientation': orientation}
	r = requests.get(url, params=params, headers={'Authorization': k}, timeout=30)
	return r.json()

def search_safe(query, per_page=15, orientation='portrait'):
	result = {"videos": []}
	try:
		result = search(query, per_page, orientation)
	except Exception:
		pass
	return result

def _best_file(video):
	files = [f for f in video.get('video_files', []) if f.get('link')]
	portrait = [f for f in files if (f.get('height',0) or 0) >= (f.get('width',0) or 0)]
	pool = portrait or files
	pool.sort(key=lambda f: abs((f.get('height',0) or 0) - 1280))
	return pool[0] if pool else None

def _long_enough(video, minsec=6):
	return (video.get('duration', 0) or 0) >= minsec

EXT = '.mp4'
PREF = 'clip'

def download(url, dest):
	data = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'}, timeout=120).content
	f = open(dest, 'wb')
	f.write(data)
	f.close()
	return dest

def _dl_one(v, d):
	bf = _best_file(v)
	vid = str(v.get('id'))
	dest = os.path.join(d, PREF + vid + EXT)
	download(bf['link'], dest) if bf else None
	return dest if bf else None

def fetch_for_topic(topic, query=None, count=3):
	q = query or topic
	d = os.path.join(LIB, str(topic).strip().lower())
	os.makedirs(d, exist_ok=True)
	cache = load_cache()
	used = set(cache.get('used', []))
	data = search_safe(q, per_page=20)
	cand = [v for v in data.get('videos', []) if str(v.get('id')) not in used]
	cand.sort(key=lambda v: (v.get('duration', 0) or 0), reverse=True)
	vids = cand[:count]
	got = [_dl_one(v, d) for v in vids]
	got = [g for g in got if g]
	used.update([str(v.get('id')) for v in vids])
	cache['used'] = list(used)
	save_cache(cache)
	return got
