# channel_loader.py - Load/validate/list channels.
import os, io, json

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CHANNELS_DIR = os.path.join(ROOT, 'channels')
REQUIRED = ['id', 'name', 'token_file', 'style', 'content', 'schedule']


def channels_dir():
	return CHANNELS_DIR


def list_channels(include_disabled=True):
	if not os.path.isdir(CHANNELS_DIR):
		return []
	out = []
	for name in sorted(os.listdir(CHANNELS_DIR)):
		if name.startswith('_'):
			continue
		p = os.path.join(CHANNELS_DIR, name, 'channel.json')
		if not os.path.exists(p):
			continue
		if not include_disabled:
			try:
				cfg = json.load(io.open(p, encoding='utf-8'))
				if not cfg.get('enabled', False):
					continue
			except Exception:
				continue
		out.append(name)
	return out


def channel_dir(cid):
	return os.path.join(CHANNELS_DIR, cid)


def load(cid):
	p = os.path.join(CHANNELS_DIR, cid, 'channel.json')
	if not os.path.exists(p):
		raise ValueError('channel not found: ' + cid)
	try:
		cfg = json.load(io.open(p, encoding='utf-8'))
	except Exception as e:
		raise ValueError('invalid json in %s: %s' % (p, e))
	missing = [k for k in REQUIRED if k not in cfg]
	if missing:
		raise ValueError('channel %s missing keys: %s' % (cid, ','.join(missing)))
	if cfg['id'] != cid:
		raise ValueError('channel id mismatch: folder=%s json=%s' % (cid, cfg['id']))
	cfg['_dir'] = channel_dir(cid)
	return cfg


def save(cid, cfg):
	p = os.path.join(CHANNELS_DIR, cid, 'channel.json')
	cfg.pop('_dir', None)
	io.open(p, 'w', encoding='utf-8').write(json.dumps(cfg, ensure_ascii=False, indent=2))
	return p


def load_content(cid, kind=None):
	p = os.path.join(CHANNELS_DIR, cid, 'content_db.json')
	if not os.path.exists(p):
		return [] if kind else {}
	db = json.load(io.open(p, encoding='utf-8'))
	if kind is None:
		return db
	return db.get(kind, [])


def load_topic_pool(cid):
	p = os.path.join(CHANNELS_DIR, cid, 'topic_pool.json')
	if not os.path.exists(p):
		return {}
	try:
		return json.load(io.open(p, encoding='utf-8'))
	except Exception:
		return {}


def token_path(cfg):
	tf = cfg.get('token_file') or 'config/token.pickle'
	if os.path.isabs(tf):
		return tf
	cid = cfg['id']
	local = os.path.join(CHANNELS_DIR, cid, os.path.basename(tf))
	if os.path.exists(local):
		return local
	return os.path.join(ROOT, tf.replace('/', os.sep))


def ensure_dirs():
	os.makedirs(CHANNELS_DIR, exist_ok=True)
	return CHANNELS_DIR


def create_from_template(new_id, name=None, token_file=None):
	import shutil
	tmpl = os.path.join(CHANNELS_DIR, '_template')
	if not os.path.isdir(tmpl):
		raise ValueError('_template not found')
	dst = os.path.join(CHANNELS_DIR, new_id)
	if os.path.exists(dst):
		raise ValueError('channel already exists: ' + new_id)
	shutil.copytree(tmpl, dst)
	cfg = json.load(io.open(os.path.join(dst, 'channel.json'), encoding='utf-8'))
	cfg['id'] = new_id
	cfg['name'] = name or new_id
	if token_file:
		cfg['token_file'] = token_file
	io.open(os.path.join(dst, 'channel.json'), 'w', encoding='utf-8').write(
		json.dumps(cfg, ensure_ascii=False, indent=2)
	)
	return dst


if __name__ == '__main__':
	ids = list_channels()
	print('Channels:', ids)
	for cid in ids:
		try:
			cfg = load(cid)
			print(' -', cid, '|', cfg['name'], '| enabled=', cfg.get('enabled'),
				'| kinds=', cfg['content'].get('kinds'))
		except Exception as e:
			print(' -', cid, 'ERROR:', e)
