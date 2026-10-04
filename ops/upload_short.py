# -- coding: utf-8 --
# Upload Shorts voi QC gate + topic dedup
import os, sys, json, time, sqlite3
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

DB = 'state/pipeline.db'

def _used_topics(channel, days=30):
	"""Tra ve set topic da dung trong N ngay qua."""
	if not os.path.exists(DB):
		return set()
	cutoff = time.time() - days * 86400
	try:
		c = sqlite3.connect(DB)
		rows = c.execute(
			'SELECT topic FROM publications WHERE channel_id=? AND created_at > datetime(?, "unixepoch")',
			(channel, int(cutoff))
		).fetchall()
		c.close()
		return set(r[0] for r in rows if r[0])
	except Exception:
		return set()

def pick_topic(channel, candidates):
	"""Chon topic chua dung trong 30 ngay."""
	used = _used_topics(channel, 30)
	for t in candidates:
		if t not in used:
			return t
	return None

def publish(video_path, title, description, tags, channel, topic, privacy='public'):
	"""Upload voi QC gate + dedup."""
	from ops import quality_check as qc
	from ops import os_publish as op
	
	# 1. QC
	q = qc.evaluate(video_path, title)
	if not q['ok']:
		return {'ok': False, 'stage': 'qc', 'errors': q['errors']}
	
	# 2. Dedup
	used = _used_topics(channel, 30)
	if topic in used:
		return {'ok': False, 'stage': 'dedup', 'err': 'topic used in 30d: ' + topic}
	
	# 3. Upload
	op.set_channel(channel)
	r = op.publish(
		video_path=video_path,
		title=title,
		description=description,
		tags=tags,
		privacy=privacy,
		topic=topic,
		force=True,
	)
	return r
