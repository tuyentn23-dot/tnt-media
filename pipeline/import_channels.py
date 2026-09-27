# -- coding: utf-8 --
# pipeline/import_channels.py - Import channels/.json vao DB
import os, sys, json, glob
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)
from pipeline import state

CH = os.path.join(ROOT, 'channels')


def find_configs():
	out = []
	for f in sorted(glob.glob(os.path.join(CH, '*.json'))):
		if 'template' in os.path.basename(f).lower():
			continue
		out.append(f)
	return out


def import_one(c, path):
	try:
		d = json.load(open(path, encoding='utf-8'))
	except Exception as e:
		print('[skip] ', path, str(e)[:80])
		return 0
	cid = d.get('name') or os.path.splitext(os.path.basename(path))[0]
	enabled = 1 if d.get('active', True) else 0
	niche = json.dumps(d.get('topics', []), ensure_ascii=False)
	forbidden = json.dumps([d.get('romance')] if d.get('romance') == 'forbidden' else [], ensure_ascii=False)
	kinds = json.dumps(d.get('topics', []), ensure_ascii=False)
	voice = json.dumps({'preset': d.get('voicePreset'), 'id': d.get('voiceId')}, ensure_ascii=False)
	maxlen = int(d.get('maxSeconds', 60))
	style = json.dumps({'aspect': d.get('aspect'), 'colorPrimary': d.get('colorPrimary'), 'colorAccent': d.get('colorAccent'), 'watermark': d.get('watermark')}, ensure_ascii=False)
	sched = json.dumps({'cron': d.get('scheduleCron')}, ensure_ascii=False)
	now = state.now()
	c.execute('INSERT OR REPLACE INTO channels (id, enabled, niche, forbidden, kinds, voice, max_length_sec, style, schedule, publish_mode, quality_gate, created_at, updated_at) VALUES (?,?,?,?,?,?,?,?,?,?,?,COALESCE((SELECT created_at FROM channels WHERE id=?),?),?)',
		(cid, enabled, niche, forbidden, kinds, voice, maxlen, style, sched, 'approve', 'normal', cid, now, now))
	return 1


def run():
	c = state.init()
	n = 0
	for f in find_configs():
		n = n + import_one(c, f)
	c.commit()
	print('[import] channels: ', n)
	rows = c.execute('SELECT id, enabled FROM channels').fetchall()
	for r in rows:
		print(' -', r[0], 'enabled=', r[1])
	return c


if __name__ == '__main__':
	run()
