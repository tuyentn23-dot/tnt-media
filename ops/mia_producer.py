# mia_producer.py - san xuat video cho kenh Mia theo style (tab)
import os, sys, json, time
sys.path.insert(0, os.getcwd())
try:
	sys.stdout.reconfigure(encoding="utf-8")
except Exception:
	pass
from ops import channel_render as CR
from ops import quality_gate as QG
from ops import os_publish as OP
from os_app import db

ROOT = os.getcwd()
CH = 'Mialinhcute'
CDB = os.path.join(ROOT, 'channels', CH, 'content_db.json')

def load_items():
	d = json.load(open(CDB, encoding='utf-8'))
	return [(k, it) for k in d for it in d[k]]

def published_ids():
	c = db.connect()
	rows = c.execute('SELECT title FROM videos WHERE youtube_id IS NOT NULL').fetchall()
	return set((r[0] or '') for r in rows)
def produce(topic, item, live=True):
	cid = str(item.get('id'))
	out = 'output/mia_' + cid + '.mp4'
	t0 = time.time()
	r = CR.render_for(CH, dict(item), out, scenes=5)
	ok = isinstance(r, str) and os.path.exists(r)
	q = QG.evaluate(r) if ok else {}
	res = {'id': cid, 'topic': topic, 'ok': ok, 'score': q.get('score'), 'sec': round(time.time()-t0,1)}
	if live and ok and q.get('passes'):
		hook = item.get('hook', '').strip().rstrip('.')
		title = hook[:90] + ' #shorts'
		tags = ['shorts', 'mialinhcute', 'cute', 'viral']
		desc = hook + chr(10) + chr(10) + ' '.join(['#'+t for t in tags])
		OP.set_channel(CH)
		pub = OP.publish(out, title, desc, tags=tags, privacy='public', topic=topic + chr(95) + cid, force=True)
		res['url'] = pub.get('url') or pub.get('error')
	return res

def run_many(limit=5, live=True):
	items = load_items()
	pubd = published_ids()
	fresh = []
	for k, it in items:
		hook = it.get('hook', '').strip().rstrip('.') + ' #shorts'
		if hook not in pubd:
			fresh.append((k, it))
	fresh = fresh[:limit]
	rows = []
	for k, it in fresh:
		try:
			rows.append(produce(k, it, live=live))
		except Exception as e:
			rows.append({'id': it.get('id'), 'ok': False, 'error': str(e)[:80]})
	return rows
