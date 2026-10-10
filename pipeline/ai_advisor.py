# pipeline/ai_advisor.py
import os, sys
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT not in sys.path:
	sys.path.insert(0, ROOT)
from pipeline import state


def suggest_metadata(pub_id):
	c = state.connect()
	row = c.execute('SELECT id, channel_id, kind, topic, title FROM publications WHERE id=?', (pub_id,)).fetchone()
	if not row:
		c.close()
		return {'ok': False, 'error': 'not found'}
	topic = (row['topic'] or '').strip()
	kind = (row['kind'] or '').strip()
	ch = row['channel_id']
	tags = set()
	f = c.execute('SELECT topic, kind FROM publications WHERE channel_id=? AND view_count > 0 ORDER BY view_count DESC LIMIT 10', (ch,)).fetchall()
	for t in f:
		if t['topic']:
			tags.add(t['topic'])
		if t['kind']:
			tags.add(t['kind'])
	c.close()
	if kind:
		tags.add(kind)
	tags.update(['shorts', 'viral', 'tiktok'])
	sugs = []
	if topic:
		sugs.append(topic.title())
		sugs.append('Bi mat ve ' + topic)
		sugs.append(topic + ' - su that ban chua biet')
		sugs.append(topic + ' #shorts')
	return {'ok': True, 'titles': sugs[:5], 'tags': sorted(tags)[:15]}


def score_video(pub_id):
	c = state.connect()
	row = c.execute('SELECT file_path, view_count, like_count FROM publications WHERE id=?', (pub_id,)).fetchone()
	c.close()
	if not row:
		return {'ok': False, 'error': 'not found'}
	score = 0
	reasons = []
	try:
		from ops import quality_gate as qg
		r = qg.evaluate(row['file_path'])
		score = int(r.get('score') or 0)
		reasons = r.get('reasons') or []
	except Exception as e:
		reasons.append('gate err: ' + str(e)[:80])
	v = row['view_count'] or 0
	lk = row['like_count'] or 0
	engagement = min(50, int((v / 100) + (lk * 2)))
	final = min(100, score + engagement)
	if final >= 80: label = 'xuat sac'
	elif final >= 60: label = 'tot'
	elif final >= 40: label = 'trung binh'
	else: label = 'yeu'
	return {'ok': True, 'score': final, 'gate': score, 'engagement': engagement, 'label': label, 'reasons': reasons[:5]}


def feedback_report(channel_id=None):
	c = state.connect()
	sql = 'SELECT topic, kind, view_count, like_count FROM publications WHERE view_count > 0'
	params = []
	if channel_id:
		sql += ' AND channel_id=?'
		params.append(channel_id)
	sql += ' ORDER BY view_count DESC LIMIT 30'
	rows = c.execute(sql, tuple(params)).fetchall()
	c.close()
	agg = {}
	for r in rows:
		t = r['topic'] or r['kind'] or 'unknown'
		if t not in agg:
			agg[t] = {'views': 0, 'likes': 0, 'count': 0}
		agg[t]['views'] += r['view_count'] or 0
		agg[t]['likes'] += r['like_count'] or 0
		agg[t]['count'] += 1
	ranked = sorted(agg.items(), key=lambda x: -x[1]['views'])
	topics = [{'topic': k, 'views': v['views'], 'likes': v['likes'], 'count': v['count']} for k, v in ranked[:10]]
	return {'ok': True, 'topics': topics, 'total': len(rows)}
