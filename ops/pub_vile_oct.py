import os, sys, json, time
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
sys.path.insert(0, os.getcwd())
from ops import quality_gate_vile as QGV
from ops import os_publish as OP
from ops.vile_content import VIDEOS
v = "output/vile_octopus.mp4"
q = QGV.evaluate(v)
print("QG:", json.dumps(q, ensure_ascii=False))
if q.get("passes"):
 OP.set_channel("vilevi5676")
 print("channel:", OP.active_channel())
 cfg = VIDEOS["octopus"]
 video = os.path.abspath(v)
 title = cfg["title"]
 desc = cfg["desc"] + chr(10) + chr(10) + "#vilevi #fact #khoahoc #bachtuoc #khampha"
 tags = cfg["tags"]
 topic = "chvilevi5676_octopus_" + time.strftime("%Y%m%d_%H%M%S")
 r = OP.publish(video, title, description=desc, tags=tags, privacy="public", topic=topic, force=True)
 print("RESULT:", json.dumps(r, ensure_ascii=False, default=str))