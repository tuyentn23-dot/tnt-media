# trend_engine.py - scan trends (google suggest + youtube autocomplete) -> topic_pool
import os, sys, json, time, urllib.request, urllib.parse
CAND = [os.environ.get("TNT_MEDIA_ROOT"), os.getcwd()] + list(sys.path)
ROOT = next((p for p in CAND if p and os.path.isdir(os.path.join(p, "memory"))), os.getcwd())
POOL = os.path.join(ROOT, "memory", "topic_pool.json")
SEEDS = ['meo', 'cho', 'anime', 'roblox', 'gacha', 'lifehack', 'bi an', 'khoa hoc', 'vu tru', 'satisfying', 'ca phe', 'am nhac']
STOP = set(['la gi', 'nhu the nao', 'o dau', 'bao nhieu'])


def _get(url, timeout=10):
	try:
		req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
		return urllib.request.urlopen(req, timeout=timeout).read().decode("utf-8", errors="replace")
	except Exception:
		return ""


def suggest(q, hl='vi'):
	u = 'https://suggestqueries.google.com/complete/search?client=firefox&hl=' + hl + '&q=' + urllib.parse.quote(q)
	r = _get(u)
	if not r:
		return []
	try:
		data = json.loads(r)
		return [s for s in data[1] if isinstance(s, str)]
	except Exception:
		return []


def scan(seeds=None):
	seeds = seeds or SEEDS
	freq = {}
	for s in seeds:
		for term in suggest(s):
			t = term.strip().lower()
			if len(t) < 3 or t in STOP:
				continue
			freq[t] = freq.get(t, 0) + 1
	return freq


def load_pool():
	if os.path.exists(POOL):
		try:
			return json.load(open(POOL, encoding="utf-8"))
		except Exception:
			pass
	return {"topics": {}, "updated": ""}


def update_pool(freq, pool=None, decay=0.9):
	pool = pool or load_pool()
	topics = pool.setdefault("topics", {})
	for k in list(topics.keys()):
		topics[k] = round(topics[k] * decay, 3)
		if topics[k] < 0.05:
			topics.pop(k, None)
	mx = max(freq.values()) if freq else 1
	for k, v in freq.items():
		topics[k] = round(min(10.0, topics.get(k, 0) + v / float(mx)), 3)
	pool["updated"] = time.strftime("%Y-%m-%dT%H:%M:%S")
	json.dump(pool, open(POOL, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
	return pool


def top_topics(n=20, pool=None):
	pool = pool or load_pool()
	topics = pool.get("topics", {})
	return sorted(topics.items(), key=lambda x: -x[1])[:n]


def refresh(seeds=None):
	freq = scan(seeds)
	pool = update_pool(freq)
	return top_topics(20, pool)
