# channel_registry.py - trung tam quan ly kenh (tab-indent)
import os, sys, json
ROOT = os.getcwd()
CH = os.path.join(ROOT, 'channels')

def list_channels():
	return sorted([d for d in os.listdir(CH) if os.path.isdir(os.path.join(CH, d)) and not d.startswith('_')])

def channel_info(cid):
	p = os.path.join(CH, cid, 'channel.json')
	cfg = json.load(open(p, encoding='utf-8')) if os.path.exists(p) else {}
	cdb = os.path.join(CH, cid, 'content_db.json')
	topics = list(json.load(open(cdb, encoding='utf-8')).keys()) if os.path.exists(cdb) else []
	return {'id': cid, 'name': cfg.get('name'), 'voice': (cfg.get('style') or {}).get('voice'), 'topics': topics}

def content_count(cid):
	cdb = os.path.join(CH, cid, 'content_db.json')
	d = json.load(open(cdb, encoding='utf-8')) if os.path.exists(cdb) else {}
	return {k: len(v) for k, v in d.items()}
def published_for(cid):
	try:
		from os_app import db
		c = db.connect()
		rows = c.execute('SELECT title, youtube_id FROM videos WHERE youtube_id IS NOT NULL').fetchall()
		return [(r[0], r[1]) for r in rows]
	except Exception:
		return []

def published_count(cid):
	cdb = os.path.join(CH, cid, 'content_db.json')
	d = json.load(open(cdb, encoding='utf-8')) if os.path.exists(cdb) else {}
	hooks = set((it.get('hook', '').strip().rstrip('.') + ' #shorts') for k in d for it in d[k])
	pub = published_for(cid)
	return len([1 for t, y in pub if t in hooks])

def registry():
	out = {}
	for cid in list_channels():
		info = channel_info(cid)
		info['content'] = content_count(cid)
		info['published'] = published_count(cid)
		out[cid] = info
	return out

def save_registry(path=None):
	path = path or os.path.join(ROOT, 'memory', 'channel_registry.json')
	json.dump(registry(), open(path, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
	return path
