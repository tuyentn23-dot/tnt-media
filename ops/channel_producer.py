# channel_producer.py - san xuat video cho BAT KY kenh nao (tab)
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

def load_items(cid):
	p = os.path.join(ROOT, 'channels', cid, 'content_db.json')
	d = json.load(open(p, encoding='utf-8'))
	return [(k, it) for k in d for it in d[k]]

def published_titles():
	c = db.connect()
	rows = c.execute('SELECT title FROM videos WHERE youtube_id IS NOT NULL').fetchall()
	return set((r[0] or '') for r in rows)
def produce(cid, topic, item, live=True):
	iid = str(item.get('id'))
	out = 'output/' + cid + '_' + iid + '.mp4'
	t0 = time.time()
	r = CR.render_for(cid, dict(item), out, scenes=5)
	ok = isinstance(r, str) and os.path.exists(r)
	q = QG.evaluate(r) if ok else {}
	res = {'channel': cid, 'id': iid, 'ok': ok, 'score': q.get('score'), 'sec': round(time.time()-t0,1)}
	if live and ok and q.get('passes'):
		hook = item.get('hook', '').strip().rstrip('.')
		title = hook[:90] + ' #shorts'
		tags = ['shorts', 'viral', 'khampha']
		desc = hook + chr(10) + chr(10) + ' '.join(['#'+t for t in tags])
		OP.set_channel(cid)
		pub = OP.publish(out, title, desc, tags=tags, privacy='public', topic=topic + chr(95) + iid, force=True)
		res['url'] = pub.get('url') or pub.get('error')
	return res

def run_many(cid, limit=5, live=True):
	items = load_items(cid)
	pubd = published_titles()
	fresh = []
	for k, it in items:
		hook = it.get('hook', '').strip().rstrip('.') + ' #shorts'
		if hook not in pubd:
			fresh.append((k, it))
	fresh = fresh[:limit]
	rows = []
	for k, it in fresh:
		try:
			rows.append(produce(cid, k, it, live=live))
		except Exception as e:
			rows.append({'id': it.get('id'), 'ok': False, 'error': str(e)[:80]})
	return rows
