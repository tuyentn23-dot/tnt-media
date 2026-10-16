# -- coding: utf-8 --
# ops/music_index.py
import os, json, hashlib, glob, random
U = chr(95)
FKEY = U + U + 'file' + U + U
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(globals()[FKEY])))
BANK = os.path.join(ROOT, 'music_bank')
INDEX = os.path.join(BANK, 'index.json')
CFG = os.path.join(ROOT, 'config', 'music_emotions.json')


def _moods():
	try:
		return json.load(open(CFG, encoding='utf-8'))
	except Exception:
		return {}


def build_index(force=False):
	if os.path.exists(INDEX) and not force:
		try:
			return json.load(open(INDEX, encoding='utf-8'))
		except Exception:
			pass
	moods = list(_moods().keys())
	if not moods:
		return {}
	files = []
	for ext in ('*.wav', '*.mp3', '*.m4a', '*.ogg'):
		files.extend(glob.glob(os.path.join(BANK, ext)))
	files.sort()
	idx = {}
	for f in files:
		name = os.path.basename(f)
		h = int(hashlib.md5(name.encode()).hexdigest(), 16)
		mood = moods[h % len(moods)]
		idx[name] = {'mood': mood, 'path': f}
	json.dump(idx, open(INDEX, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
	return idx


def detect_mood(topic='', text=''):
	s = (str(topic) + ' ' + str(text)).lower()
	moods = _moods()
	best = None
	best_n = 0
	for mk, mv in moods.items():
		n = 0
		for kw in mv.get('keywords', []):
			if kw in s:
				n += 1
		if n > best_n:
			best_n = n
			best = mk
	return best or 'joy'


def pick(topic='', text='', job_id=''):
	idx = build_index()
	if not idx:
		return None
	mood = detect_mood(topic, text)
	cands = [v['path'] for k, v in idx.items() if v.get('mood') == mood and os.path.exists(v['path'])]
	if not cands:
		cands = [v['path'] for v in idx.values() if os.path.exists(v['path'])]
	seed = str(job_id or '') + '|' + str(topic or '')
	random.seed(seed)
	return random.choice(sorted(cands)) if cands else None
