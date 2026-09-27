# -- coding: utf-8 --
# pipeline/modules_loader.py - Discover + validate modules
import os, sys, importlib.util
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODULES_DIR = os.path.join(ROOT, 'modules')

REQUIRED_KEYS = ['name', 'version', 'interface']


def discover():
	res = {}
	if not os.path.isdir(MODULES_DIR):
		return res
	for cat in sorted(os.listdir(MODULES_DIR)):
		cd = os.path.join(MODULES_DIR, cat)
		if not os.path.isdir(cd):
			continue
		for fn in sorted(os.listdir(cd)):
			if not fn.endswith('.py') or fn.startswith('_'):
				continue
			path = os.path.join(cd, fn)
			mod = load_module(path, cat + '.' + fn[:-3])
			if mod is None:
				continue
			meta = getattr(mod, 'MODULE', None)
			if not meta:
				continue
			ok, msg = validate(meta)
			res[meta.get('name', fn)] = {
				'path': path,
				'category': cat,
				'meta': meta,
				'valid': ok,
				'error': msg,
			}
	return res


def load_module(path, name):
	try:
		spec = importlib.util.spec_from_file_location(name, path)
		mod = importlib.util.module_from_spec(spec)
		spec.loader.exec_module(mod)
		return mod
	except Exception as e:
		print('[load err] ', path, str(e)[:100])
		return None


def validate(meta):
	if not isinstance(meta, dict):
		return False, 'MODULE khong phai dict'
	miss = [k for k in REQUIRED_KEYS if k not in meta]
	if miss:
		return False, 'thieu key: ' + str(miss)
	return True, 'OK'


if __name__ == '__main__':
	mods = discover()
	print('found ' + str(len(mods)) + ' modules')
	for k, v in mods.items():
		print(' -', k, 'v=' + str(v['meta'].get('version')), 'valid=' + str(v['valid']))
