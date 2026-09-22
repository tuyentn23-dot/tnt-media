# mass_producer.py - auto render+gate+upload (tab-indent)
import os, sys, json, time
sys.path.insert(0, os.getcwd())
try:
	sys.stdout.reconfigure(encoding="utf-8")
except Exception:
	pass
from ops import ffmpeg_render as FR
from ops import quality_gate as QG
from ops import os_publish as OP

ROOT = os.getcwd()
DB = os.path.join(ROOT, 'memory', 'content_db.json')

def published_paths():
	try:
		from os_app import db
		c = db.connect()
		rows = c.execute('SELECT path FROM videos WHERE youtube_id IS NOT NULL').fetchall()
		return set(os.path.basename((r[0] or '')) for r in rows)
	except Exception:
		return set()

def published_topics():
	try:
		from os_app import db
		c = db.connect()
		q = 'SELECT DISTINCT lower(topic) FROM videos WHERE youtube_id IS NOT NULL'
		rows = c.execute(q).fetchall()
		return set(r[0] for r in rows)
	except Exception:
		return set()

def load():
	return json.load(open(DB, encoding='utf-8'))

def produce(topic, item, live=True):
	cid = str(item.get('id'))
	out = 'output/v' + chr(95) + cid + '.mp4'
	t0 = time.time()
	r = FR.render(dict(item), out, seed=abs(hash(cid)) % 9999, scenes=5)
	ok = isinstance(r, str) and os.path.exists(r)
	q = QG.evaluate(r) if ok else {}
	res = {'id': cid, 'topic': topic, 'ok': ok, 'score': q.get('score'), 'sec': round(time.time()-t0,1)}
	if live and ok and q.get('passes'):
		hook = item.get('hook', '').strip().rstrip('.')
		title = hook[:90] + ' #shorts'
		tags = ['shorts', 'viral', 'khampha', 'suthat']
		desc = hook + chr(10) + chr(10) + ' '.join(['#'+t for t in tags])
		pub = OP.publish(out, title, desc, tags=tags, privacy='public', topic=topic + chr(95) + cid + chr(95) + str(int(time.time())), force=True)
		res['url'] = pub.get('url') or pub.get('error')
	return res
def run_many(limit=5, live=True):
	d = load()
	pub = published_topics()
	paths = published_paths()
	items = [(it.get('topic', '') or k, it) for k in d for it in d[k]]
	fresh = [(tp, it) for (tp, it) in items if (chr(118)+chr(95)+str(it.get('id'))+'.mp4') not in paths][:limit]
	rows = []
	for tp, it in fresh:
		try:
			rows.append(produce(tp, it, live=live))
		except Exception as e:
			rows.append({'id': it.get('id'), 'topic': tp, 'ok': False, 'error': str(e)[:80]})
	return rows


