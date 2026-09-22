import os, sys, json, time
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
sys.path.insert(0, os.getcwd())
from ops import quality_gate as QG
from ops import os_publish as OP
from ops.content_v2 import VIDEOS2
v = "output/Mialinhcute_v2_cool.mp4"
q = QG.evaluate(v)
print("QG:", q.get("score"), q.get("passes"))
if q.get("passes"):
 OP.set_channel("Mialinhcute")
 cfg = VIDEOS2["cool"]
 video = os.path.abspath(v)
 title = cfg["title"]
 desc = cfg["desc"] + chr(10) + chr(10) + "#gacha #cool #school #shorts #viral #aesthetic"
 tags = cfg["tags"]
 topic = "chMialinhcute_v2_cool_" + time.strftime("%Y%m%d_%H%M%S")
 r = OP.publish(video, title, description=desc, tags=tags, privacy="public", topic=topic, force=True)
 print("RESULT:", json.dumps(r, ensure_ascii=False, default=str))