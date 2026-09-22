import os, sys, json, time
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
sys.path.insert(0, os.getcwd())
from ops import quality_gate as QG
from ops import os_publish as OP
from ops.mia_content_kids import VIDEOS
v = "output/Mialinhcute_kids_gacha_school.mp4"
q = QG.evaluate(v)
print("QG:", q.get("score"), q.get("passes"), q.get("reasons"))
if q.get("passes"):
 OP.set_channel("Mialinhcute")
 cfg = VIDEOS["gacha_school"]
 title = cfg["title"]
 desc = cfg["desc"] + chr(10) + chr(10) + "#gacha #gachaclub #school #shorts #kids #cute"
 tags = cfg["tags"]
 topic = "chMialinhcute_gacha_school_" + time.strftime("%Y%m%d_%H%M%S")
 r = OP.publish(os.path.abspath(v), title, description=desc, tags=tags, privacy="public", topic=topic, force=True)
 print("RESULT:", json.dumps(r, ensure_ascii=False, default=str))