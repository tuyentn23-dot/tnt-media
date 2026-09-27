# -- coding: utf-8 --
"""TNT Media OS - pick a fresh, viral-friendly topic not yet published."""
import os
import sys
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)

# Higher = more Shorts-friendly / higher viral potential
VIRAL_WEIGHT = dict([
    ('brain', 96), ('psychology', 94), ('shark', 95), ('space', 92), ('satisfying', 90),
    ('satisfy2', 88), ('animal', 85), ('ocean', 84),
    ('brain', 82), ('psychology', 80), ('fire', 78),
    ('cat', 76), ('dog', 76), ('spider', 74), ('snake', 93),
    ('water', 72), ('body', 70), ('food', 68),
    ('magic', 66), ('coffee', 60), ('abstract', 55),
])
DEFAULT_WEIGHT = 50


def trend_scores():
	import json, os as _os
	p = _os.path.join(ROOT, 'memory', 'topic_pool.json')
	if not _os.path.exists(p):
		return {}
	try:
		return json.load(open(p, encoding='utf-8')).get('topics', {}) or {}
	except Exception:
		return {}


def trend_boost(topic, scores):
	t = (topic or '').strip().lower()
	if not t or not scores:
		return 0.0
	best = 0.0
	for term, sc in scores.items():
		tl = term.lower()
		if t in tl or tl in t:
			best = max(best, float(sc))
	return round(best * 3.0, 3)

def library_topics():
    base = os.path.join(ROOT, 'library')
    out = []
    for d in sorted(os.listdir(base)):
        p = os.path.join(base, d)
        if not os.path.isdir(p):
            continue
        mp4 = [f for f in os.listdir(p) if f.lower().endswith('.mp4')]
        if mp4:
            out.append((d, len(mp4)))
    return out

def used_topics():
    try:
        from os_app import db
        c = db.connect()
        rows = c.execute('SELECT DISTINCT topic FROM videos WHERE topic IS NOT NULL').fetchall()
        return set((r[0] or '').strip().lower() for r in rows)
    except Exception:
        return set()

def pick(exclude=None, prefer_viral=True):
    topics = library_topics()
    used = used_topics()
    ex = set((x or '').strip().lower() for x in (exclude or []))
    cand = [(t, n) for (t, n) in topics if t.lower() not in used and t.lower() not in ex]
    if not cand:
        cand = [(t, n) for (t, n) in topics if t.lower() not in ex]
    if not cand:
        return None
    _ts = trend_scores()
    if prefer_viral:
        def score(item):
            t, n = item
            w = VIRAL_WEIGHT.get(t.lower(), DEFAULT_WEIGHT)
            return w + min(n, 10) + trend_boost(t, _ts)
        cand.sort(key=score, reverse=True)
    return cand[0][0]

if __name__ == '__main__':
    import json
    sys.stdout.buffer.write(json.dumps(dict(topics=library_topics(), used=sorted(used_topics()), pick=pick()), ensure_ascii=False).encode('utf-8'))