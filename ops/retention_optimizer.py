# retention_optimizer.py - hoc tu metrics de toi uu retention (tab)
import os, sys, json, re
ROOT = os.getcwd()
SNAP = os.path.join(ROOT, 'memory', 'metrics_snapshot.json')

def load():
	return json.load(open(SNAP, encoding='utf-8')) if os.path.exists(SNAP) else []

def top(n=10):
	d = load()
	return sorted(d, key=lambda x: x.get('views', 0), reverse=True)[:n]

def topic_stats():
	d = load()
	by = {}
	for x in d:
		t = (x.get('topic') or '').split(chr(95))[0]
		by.setdefault(t, []).append(x)
	out = {}
	for t, v in by.items():
		vs = sum(x.get('views', 0) for x in v)
		ls = sum(x.get('likes', 0) for x in v)
		out[t] = {'n': len(v), 'avg_views': round(vs / len(v), 1), 'like_rate': round(ls / max(1, vs) * 100, 2)}
	return out
def hook_words(n=15):
	d = top(n)
	words = {}
	for x in d:
		for w in re.findall(r'\w+', (x.get('title') or '').lower()):
			words[w] = words.get(w, 0) + 1
	return sorted(words.items(), key=lambda kv: -kv[1])[:20]

def recommendations():
	ts = topic_stats()
	best = sorted(ts.items(), key=lambda kv: -kv[1]['avg_views'])[:3]
	worst = sorted(ts.items(), key=lambda kv: kv[1]['avg_views'])[:3]
	return {'best_topics': best, 'worst_topics': worst, 'top_hooks': [(x['title'], x['views']) for x in top(5)]}

if __name__ == '__main__':
	import sys
	sys.stdout.reconfigure(encoding='utf-8')
	import json as _j
	print(_j.dumps(recommendations(), ensure_ascii=False, indent=1))
