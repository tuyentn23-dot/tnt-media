import os, sys, json, time
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
sys.path.insert(0, os.getcwd())
from ops import quality_gate_vile as QGV
from ops import os_publish as OP
from ops.vile_content import VIDEOS
OP.set_channel("vilevi5676")
print("channel:", OP.active_channel())
results = []
for vid in ["moon", "shark", "brain", "heart"]:
	v = os.path.abspath("output/vile_short_" + vid + ".mp4")
	q = QGV.evaluate(v)
	print(vid, "QG:", q.get("score"), q.get("passes"))
	if not q.get("passes"):
		results.append({vid: "qg_fail"})
		continue
	cfg = VIDEOS[vid]
	title = cfg["title"]
	desc = cfg["desc"] + chr(10) + chr(10) + "#vilevi #fact #khoahoc #shorts #khampha"
	tags = cfg["tags"]
	topic = "chvilevi5676_" + vid + "" + time.strftime("%Y%m%d%H%M%S")
	try:
		r = OP.publish(v, title, description=desc, tags=tags, privacy="public", topic=topic, force=True)
		results.append({vid: r.get("youtube_id"), "url": r.get("url")})
		print(vid, "PUBLISHED:", r.get("youtube_id"))
	except Exception as e:
		results.append({vid: "ERR " + str(e)[:60]})
	time.sleep(2)
print(json.dumps(results, ensure_ascii=False, indent=2))