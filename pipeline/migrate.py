# -- coding: utf-8 --
# pipeline/migrate.py - Import 4 ledger cu vao state/pipeline.db
import os, sys, json
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)
from pipeline import state

CH = os.path.join(ROOT, 'channels')
MEM = os.path.join(ROOT, 'memory')


def ledgers():
	ps = []
	if os.path.isdir(CH):
		for nm in sorted(os.listdir(CH)):
			p = os.path.join(CH, nm, 'published_ledger.json')
			if os.path.exists(p):
				ps.append(p)
	gp = os.path.join(MEM, 'published_ledger.json')
	if os.path.exists(gp):
		ps.append(gp)
	return ps


def migrate():
	c = state.init()
	ins = 0
	skipped = 0
	for lp in ledgers():
		try:
			d = json.load(open(lp, encoding='utf-8'))
		except Exception as e:
			print('[skip] ', lp, str(e)[:80])
			continue
		sigs = d.get('signatures', {}) if isinstance(d, dict) else {}
		for sig, v in sigs.items():
			if not isinstance(v, dict):
				continue
			yt = v.get('youtube_id')
			ch = v.get('channel')
			kind = v.get('kind')
			topic = v.get('topic')
			fp = v.get('file')
			ts = v.get('ts')
			try:
				c.execute('INSERT OR IGNORE INTO publications (channel_id, signature, topic, kind, youtube_id, file_path, status, published_at, created_at) VALUES (?,?,?,?,?,?,?,?,?)', (ch, sig, topic, kind, yt, fp, 'published', ts, state.now()))
				ins = ins + c.total_changes
			except Exception as e:
				print('[err] ', sig, str(e)[:80])
				skipped = skipped + 1
	c.commit()
	print('[migrate] inserted: ', ins, ' skipped: ', skipped)
	rows = c.execute('SELECT COUNT(*) FROM publications').fetchone()
	print('[migrate] total publications: ', rows[0])
	return c


if __name__ == '__main__':
	migrate()
