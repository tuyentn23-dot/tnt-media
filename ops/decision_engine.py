# -- coding: utf-8 --
"""decision_engine - chon topic/format/gio tot nhat tu trends + weights (YC4)."""
import sqlite3, os, json, sys
from datetime import datetime
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(sys.argv[0])))
if not os.path.isdir(os.path.join(ROOT, 'ops')):
	ROOT = os.getcwd()
DB = os.path.join(ROOT, 'system', 'state.db')
FM = ['shorts_fact', 'shorts_top5', 'shorts_story', 'shorts_quiz']
HOURS = [9, 15, 21]
def now(): return datetime.now().isoformat(timespec='seconds')

def pick_hour(score):
	i = int(round(score * (len(HOURS) - 1)))
	return HOURS[max(0, min(len(HOURS) - 1, i))]

def _load_weights(con, channel_id):
	row = con.execute('SELECT weightsJson FROM channels WHERE id=?', (channel_id,)).fetchone()
	if not row or not row[0]:
		return {}, {}
	try:
		w = json.loads(row[0])
	except Exception:
		return {}, {}
	return w.get('topic', {}) or {}, w.get('format', {}) or {}

def decide(channel_id, top_n=3):
	con = sqlite3.connect(DB)
	con.row_factory = sqlite3.Row
	trends = con.execute('SELECT id, topic, score FROM trends ORDER BY score DESC, id DESC LIMIT ?', (top_n * 8,)).fetchall()
	tw, fw = _load_weights(con, channel_id)
	con.execute('DELETE FROM decisions WHERE channelId = ?', (channel_id,))
	made = []
	scored = []
	for t in trends:
		topic = t['topic']
		tscore = float(t['score'] or 0)
		boost = float(tw.get(topic, 1.0))
		scored.append((tscore * boost, topic, t))
	scored.sort(key=lambda x: x[0], reverse=True)
	for i, (final, topic, t) in enumerate(scored[:top_n]):
		fmt = FM[i % len(FM)]
		fboost = float(fw.get(fmt, 1.0))
		score = round(min(1.0, final / (final + 1.0) + 0.1 * fboost), 3)
		hook = topic
		hour = pick_hour(score)
		rat = json.dumps({'hour': hour, 'topic_weight': tw.get(topic, 1.0), 'format_weight': fboost}, ensure_ascii=False)
		snap = json.dumps(dict(topic=tw, format=fw), ensure_ascii=False)
		con.execute('INSERT INTO decisions (channelId, trendId, topic, format, hook, score, weightsSnapshotJson, rationale, chosenAt) VALUES (?,?,?,?,?,?,?,?,?)', (channel_id, t['id'], topic, fmt, hook, score, snap, rat, now()))
		made.append(dict(topic=topic, format=fmt, score=score, hour=hour))
	con.execute('INSERT INTO changelog (version, entity, change, actor, createdAt) VALUES (?,?,?,?,?)', ('decision_engine', 'decisions', 'made ' + str(len(made)) + ' with weights', 'agent', now()))
	con.commit()
	con.close()
	return made

if os.path.basename(sys.argv[0]).startswith('decision_engine'):
	cid = int(sys.argv[1]) if len(sys.argv) > 1 else 1
	print(json.dumps(decide(cid), ensure_ascii=False, indent=1))
