# content_freshness.py - per-channel ledger + global fallback
import os, io, sys, json, time
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)
GLOBAL_LEDGER = os.path.join(ROOT, 'memory', 'published_ledger.json')
CHANNELS_DIR = os.path.join(ROOT, 'channels')

_ACTIVE_CHANNEL = None


def set_channel(cid):
	global _ACTIVE_CHANNEL
	_ACTIVE_CHANNEL = cid
	return cid


def active_channel():
	return _ACTIVE_CHANNEL


def _ledger_path():
	if _ACTIVE_CHANNEL:
		d = os.path.join(CHANNELS_DIR, _ACTIVE_CHANNEL)
		if os.path.isdir(d):
			return os.path.join(d, 'published_ledger.json')
	return GLOBAL_LEDGER


def _load():
	p = _ledger_path()
	if os.path.exists(p):
		try:
			return json.load(io.open(p, encoding='utf-8'))
		except Exception:
			pass
	return {'signatures': {}}


def _save(dd):
	p = _ledger_path()
	os.makedirs(os.path.dirname(p), exist_ok=True)
	io.open(p, 'w', encoding='utf-8').write(json.dumps(dd, ensure_ascii=False, indent=2))


def signature(item, kind):
	h = (item.get('hook') or '').strip().lower()[:40]
	return kind + '|' + str(item.get('id', '')) + '|' + h


def is_published(sig):
	return sig in _load()['signatures']


def mark_published(sig, meta):
	dd = _load()
	meta['ts'] = time.strftime('%Y-%m-%dT%H:%M:%S')
	meta['channel'] = _ACTIVE_CHANNEL or '_global'
	dd['signatures'][sig] = meta
	_save(dd)


def published_count():
	return len(_load()['signatures'])


def published_signatures():
	return list(_load()['signatures'].keys())


def reset():
	_save({'signatures': {}})


def fresh_items(kind, limit=None, source=None):
	if source is None:
		from ops.content_video5 import load as _legacy_load
		items = _legacy_load(kind)
	else:
		items = source
	out = []
	for it in items:
		sig = signature(it, kind)
		if is_published(sig):
			continue
		out.append(it)
		if limit and len(out) >= limit:
			break
	return out
