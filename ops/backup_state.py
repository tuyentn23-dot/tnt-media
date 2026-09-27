# -- coding: utf-8 --
# ops/backup_state.py - Backup SQLite dung chuan WAL (khong copy rieng file DB)
import os, sys, sqlite3, time, argparse, json
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)


def backup_sqlite(src, dst_dir):
	os.makedirs(dst_dir, exist_ok=True)
	name = os.path.basename(src).replace('.db', '')
	ts = time.strftime('%Y%m%d_%H%M%S')
	dst = os.path.join(dst_dir, name + '_' + ts + '.db')
	src_conn = sqlite3.connect(src, timeout=30)
	try:
		src_conn.execute('PRAGMA wal_checkpoint(TRUNCATE)')
	except Exception:
		pass
	dst_conn = sqlite3.connect(dst)
	try:
		src_conn.backup(dst_conn)
	finally:
		dst_conn.close()
		src_conn.close()
	return dst


def verify(path):
	c = sqlite3.connect(path)
	try:
		rows = c.execute("SELECT name FROM sqlite_master WHERE type='table'").fetchall()
		counts = {}
		for r in rows:
			t = r[0]
			try:
				counts[t] = c.execute('SELECT COUNT(*) FROM ' + t).fetchone()[0]
			except Exception:
				counts[t] = -1
		return counts
	finally:
		c.close()


def main():
	ap = argparse.ArgumentParser()
	ap.add_argument('--src', default=os.path.join(ROOT, 'state', 'pipeline.db'))
	ap.add_argument('--dst-dir', default=os.path.join(ROOT, 'backups'))
	ap.add_argument('--verify', action='store_true')
	args = ap.parse_args()
	if not os.path.exists(args.src):
		print(json.dumps({'ok': False, 'error': 'src not found: ' + args.src}))
		return 1
	dst = backup_sqlite(args.src, args.dst_dir)
	res = {'ok': True, 'src': args.src, 'dst': dst, 'bytes': os.path.getsize(dst)}
	if args.verify:
		res['tables'] = verify(dst)
	print(json.dumps(res, ensure_ascii=False))
	return 0


if __name__ == '__main__':
	sys.exit(main())
