import os, sys, json, time
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
sys.path.insert(0, os.getcwd())
from ops import quality_gate as QG
from ops import os_publish as OP
from ops.content_v2 import VIDEOS2
v = "output/Mialinhcute_v2_love.mp4"
q = QG.evaluate(v)
print("QG:", json.dumps(q, ensure_ascii=False))
if q.get("passes"):
 OP.set_channel("Mialinhcute")
 cfg = VIDEOS2["love"]
 video = os.path.abspath(v)
 title = cfg["title"]
 desc = cfg["desc"] + chr(10) + chr(10) + "#gacha #love #crush #shorts #viral #romantic"
 tags = cfg["tags"]
 topic = "chMialinhcute_v2_love_" + time.strftime("%Y%m%d_%H%M%S")
 r = OP.publish(video, title, description=desc, tags=tags, privacy="public", topic=topic, force=True)
 print("RESULT:", json.dumps(r, ensure_ascii=False, default=str))