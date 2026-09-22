# evolve.py - self-improvement (MAPE-K) + multi-signal learning
import os, io, sys, json, time, sqlite3
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)
MODEL = os.path.join(ROOT,"memory","evolve_model.json")
DBV = os.path.join(ROOT,"memory","tnt_media.db")
try:
	from ops import yt_analytics as _ya
except Exception:
	_ya = None
LEDGER = os.path.join(ROOT,"memory","published_ledger.json")

def _load():
	try: return json.load(io.open(MODEL,encoding="utf-8"))
	except Exception: return {}
def _save(m):
	m["updated"]=time.strftime("%Y-%m-%dT%H:%M:%S")
	io.open(MODEL,"w",encoding="utf-8").write(json.dumps(m,ensure_ascii=False,indent=2))

def collect():
	c=sqlite3.connect(DBV)
	rows=list(c.execute("select topic,title,youtube_id,created_at from videos where youtube_id is not null"))
	return rows

def analyze():
	rows=collect()
	m=_load()
	from collections import Counter
	cnt=Counter(); hours=Counter(); kinds=Counter()
	for tp,title,yid,ts in rows:
		if tp: cnt[tp]+=1
		if tp and tp.startswith("ashort"):
			parts=tp.split("_")
			if len(parts)>=3: kinds[parts[1]]+=1
		if ts:
			h=(ts or "")[11:13]
			hours[h]+=1
	m["topic_counts"]=dict(cnt.most_common(40))
	m["kinds"]=dict(kinds)
	m["hours"]=dict(hours.most_common())
	m["total_published"]=len(rows)
	if _ya:
		r=_ya.fetch(28)
		if r.get("ok"):
			m["yt_views"]=r.get("rows",[])[:50]
	_save(m)
	return m

def suggest():
	m=_load()
	tc=m.get("topic_counts",{})
	kw="whatif"
	kf="facts"
	wf=sum(v for k,v in tc.items() if kw in k)
	ft=sum(v for k,v in tc.items() if kf in k)
	prefer=kf if wf>=ft else kw
	hours=m.get("hours",{})
	best_hour=max(hours,key=hours.get) if hours else "12"
	return {"prefer_kind":prefer,"best_hour":best_hour,"whatif_done":wf,"facts_done":ft}

def run_once():
	m=analyze()
	s=suggest()
	m["last_suggest"]=s
	_save(m)
	return {"analyzed":True,"suggest":s}