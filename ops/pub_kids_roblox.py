import os, sys, json, time
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
sys.path.insert(0, os.getcwd())
from ops import quality_gate as QG
from ops import os_publish as OP
from ops.mia_content_kids import VIDEOS
def pub(vid, fname):
	v = "output/" + fname
	q = QG.evaluate(v)
	print(vid, "QG:", q.get("score"), q.get("passes"))
	if not q.get("passes"):
		print(vid, "FAIL", q.get("reasons"))
		return
	OP.set_channel("Mialinhcute")
	cfg = VIDEOS[vid]
	title = cfg["title"]
	desc = cfg["desc"] + chr(10) + chr(10) + "#roblox #game #shorts #viral #kids"
	tags = cfg["tags"]
	topic = "chMialinhcute_kids_" + vid + "" + time.strftime("%Y%m%d%H%M%S")
	r = OP.publish(os.path.abspath(v), title, description=desc, tags=tags, privacy="public", topic=topic, force=True)
	print(vid, "PUBLISHED:", r.get("youtube_id"))
pub("roblox_doors", "Mialinhcute_kids_roblox_doors.mp4")