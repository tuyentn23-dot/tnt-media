# ops/update_state.py - tu dong cap nhat STATE.md tu ledger
import os, sys, json, time
sys.path.insert(0, os.getcwd())
from ops import state_mgr as SM
def load_ledger(cid):
	p = os.path.join("channels", cid, "published_ledger.json")
	if not os.path.exists(p):
		return {}
	return json.load(open(p, encoding="utf-8"))

def recent(cid, hours=24):
	led = load_ledger(cid)
	sigs = led.get("signatures", {})
	cutoff = time.time() - hours * 3600
	out = []
	for k, v in sigs.items():
		ts_str = v.get("ts", "")
		try:
			ts = time.mktime(time.strptime(ts_str[:19], "%Y-%m-%dT%H:%M:%S"))
		except:
			continue
		if ts >= cutoff:
			out.append({"id": v.get("youtube_id"), "title": k.split(chr(124))[-1][:60], "ts": ts_str[:16]})
	return out

if __name__ == "__main__":
	channels = ["Mialinhcute", "vilevi5676"]
	all_recent = {}
	for c in channels:
		all_recent[c] = recent(c, hours=24)
		print(c, len(all_recent[c]), "video 24h qua")
	r = SM.check()
	print("STATE.md check:", r)