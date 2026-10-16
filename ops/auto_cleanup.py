# -- coding: utf-8 --
# ops/auto_cleanup.py - Tu dong don video da publish (phuong an C)
import os, shutil, time, datetime
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUTPUT = os.path.join(ROOT, 'output')
TRASH = os.path.join(ROOT, '_trash', 'auto_cleanup')
GRACE_DAYS = 14
SIZE_LIMIT_GB = 2.0
TRASH_KEEP_DAYS = 60


def _db():
	import sqlite3
	return sqlite3.connect(os.path.join(ROOT, 'state', 'pipeline.db'))


def _published_paths():
	conn = _db()
	rows = conn.execute("SELECT file_path FROM publications WHERE youtube_id IS NOT NULL AND youtube_id != '' AND file_path IS NOT NULL").fetchall()
	conn.close()
	out = set()
	for (p,) in rows:
		if p:
			out.add(os.path.basename(p))
	return out


def _dir_size(path):
	total = 0
	for f in os.listdir(path):
		fp = os.path.join(path, f)
		if os.path.isfile(fp):
			total += os.path.getsize(fp)
	return total


def _move_to_trash(path):
	os.makedirs(TRASH, exist_ok=True)
	dst = os.path.join(TRASH, os.path.basename(path))
	if os.path.exists(dst):
		dst = dst + '.' + str(int(time.time()))
	shutil.move(path, dst)
	return dst


def _clean_trash():
	if not os.path.isdir(TRASH):
		return 0
	cutoff = time.time() - TRASH_KEEP_DAYS * 86400
	n = 0
	for f in os.listdir(TRASH):
		fp = os.path.join(TRASH, f)
		if os.path.isfile(fp) and os.path.getmtime(fp) < cutoff:
			os.remove(fp)
			n += 1
	return n


def run(dry_run=False, grace_days=GRACE_DAYS, size_limit_gb=SIZE_LIMIT_GB):
	if not os.path.isdir(OUTPUT):
		return {'ok': False, 'error': 'no output dir'}
	published = _published_paths()
	now = time.time()
	cutoff = now - grace_days * 86400
	moved = []
	# Buoc 1: xoa video da publish qua grace period
	for f in os.listdir(OUTPUT):
		if not f.endswith('.mp4') or f.startswith(''):
			continue
		if f not in published:
			continue
		fp = os.path.join(OUTPUT, f)
		if os.path.getmtime(fp) < cutoff:
			if not dry_run:
				_move_to_trash(fp)
			moved.append(f)
	# Buoc 2: neu vuot size limit, xoa them (cu nhat truoc)
	size_gb = _dir_size(OUTPUT) / (1024 ** 3)
	if size_gb > size_limit_gb:
		cands = []
		for f in os.listdir(OUTPUT):
			if not f.endswith('.mp4') or f.startswith(''):
				continue
			if f not in published:
				continue
			fp = os.path.join(OUTPUT, f)
			if f in moved:
				continue
			cands.append((os.path.getmtime(fp), fp, f))
		cands.sort()
		target = size_limit_gb * 0.5 * (1024 ** 3)
		cur = _dir_size(OUTPUT)
		for mt, fp, f in cands:
			if cur <= target:
				break
			if not dry_run:
				_move_to_trash(fp)
			cur -= os.path.getsize(fp)
			moved.append(f)
	# Buoc 3: don trash cu
	trashed = 0 if dry_run else _clean_trash()
	return {'ok': True, 'moved': len(moved), 'files': moved[:20], 'trash_cleaned': trashed, 'size_after_mb': round(_dir_size(OUTPUT) / (1024 * 1024), 1), 'dry_run': dry_run}


if __name__ == '__main__':
	import sys, json
	dry = '--apply' not in sys.argv
	r = run(dry_run=dry)
	print(json.dumps(r, ensure_ascii=False, indent=2))
