# -- coding: utf-8 --
# pipeline/mversion.py - Module versioning + rollback
import os, sys, json, time, shutil, hashlib
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)
from pipeline import state
SNAP = os.path.join(ROOT, 'state', 'snapshots')


def _sha(path):
	h = hashlib.sha1()
	with open(path, 'rb') as f:
		h.update(f.read())
	return h.hexdigest()[:12]


def snapshot(module_path, version, note=''):
	os.makedirs(SNAP, exist_ok=True)
	rel = os.path.relpath(module_path, ROOT).replace(os.sep, '/')
	flat = rel.replace('/', '')
	dest = os.path.join(SNAP, flat + '.' + version + '.bak')
	shutil.copy2(module_path, dest)
	c = state.init()
	meta = json.dumps({ 'sha': _sha(module_path), 'note': note, 'rel': rel })
	c.execute('INSERT OR REPLACE INTO modules_ver (name, version, installed_at, meta) VALUES (?,?,?,?)', (rel, version, state.now(), meta))
	c.commit()
	return dest


def list_versions(name=None):
	c = state.connect()
	if name:
		rows = c.execute('SELECT name, version, installed_at FROM modules_ver WHERE name=? ORDER BY installed_at DESC', (name,)).fetchall()
	else:
		rows = c.execute('SELECT name, version, installed_at FROM modules_ver ORDER BY installed_at DESC').fetchall()
	return [dict(r) for r in rows]


def rollback(module_path, version):
	rel = os.path.relpath(module_path, ROOT).replace(os.sep, '/')
	flat = rel.replace('/', '')
	src = os.path.join(SNAP, flat + '.' + version + '.bak')
	if not os.path.exists(src):
		return { 'ok': False, 'error': 'snapshot not found: ' + src }
	shutil.copy2(src, module_path)
	c = state.init()
	c.execute('INSERT INTO audit (session, actor, action, target, version_to, reason, ts) VALUES (?,?,?,?,?,?,?)', ('pipeline', 'mversion', 'rollback', rel, version, 'manual rollback', state.now()))
	c.commit()
	return { 'ok': True, 'restored': rel, 'version': version }


if __name__ == '__main__':
	print('versions:', list_versions())
