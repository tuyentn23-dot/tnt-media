# -- coding: utf-8 --
"""weights_tuner - YC4: hoc weights tu analytics that, ghi channels.weightsJson."""
import os, sys, json, sqlite3
from datetime import datetime
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(sys.argv[0])))
if not os.path.isdir(os.path.join(ROOT, 'ops')):
	ROOT = os.getcwd()
sys.path.insert(0, ROOT)
A = os.path.join(ROOT, 'memory', 'tnt_media.db')
B = os.path.join(ROOT, 'system', 'state.db')

def _metrics():
	con = sqlite3.connect(A)
	rows = con.execute('SELECT v.topic, v.format, m.views, m.likes, m.comments FROM metrics m JOIN videos v ON v.id = m.video_id').fetchall()
	con.close()
	return rows

def _agg(rows):
	bt = {}
	bf = {}
	for topic, fmt, views, likes, comments in rows:
		v = views or 0
		l = likes or 0
		c = comments or 0
		s = float(v) + 5.0 * float(l) + 8.0 * float(c)
		bt.setdefault(topic or '', []).append(s)
		bf.setdefault(fmt or '', []).append(s)
	def avg(d):
		return {k: round(sum(v) / max(1, len(v)), 3) for k, v in d.items()}
	return avg(bt), avg(bf)

def _norm(d):
	if not d:
		return {}
	mx = max(d.values()) or 1.0
	return {k: round(0.5 + 0.5 * (v / mx), 3) for k, v in d.items()}

def tune():
	rows = _metrics()
	tw, fw = _agg(rows)
	tw = _norm(tw)
	fw = _norm(fw)
	con = sqlite3.connect(B)
	chans = list(con.execute('SELECT id, name FROM channels'))
	out = []
	for cid, name in chans:
		w = dict(topic=tw, format=fw)
		con.execute('UPDATE channels SET weightsJson=?, updatedAt=? WHERE id=?', (json.dumps(w), datetime.now().isoformat(timespec='seconds'), cid))
		out.append(dict(channel=name, topics=len(tw), formats=len(fw)))
	con.execute('INSERT INTO changelog (version, entity, change, actor, createdAt) VALUES (?,?,?,?,?)', ('weights_tuner', 'channels', 'weights from analytics', 'agent', datetime.now().isoformat(timespec='seconds')))
	con.commit()
	con.close()
	return dict(ok=True, topic_weights=tw, format_weights=fw, channels=out)

if os.path.basename(sys.argv[0]).startswith('weights_tuner'):
	print(json.dumps(tune(), ensure_ascii=False, indent=1))
