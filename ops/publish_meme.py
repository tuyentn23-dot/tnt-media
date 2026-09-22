import os, sys, json, time
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
sys.path.insert(0, os.getcwd())
from ops import os_publish as OP
from ops.content_v2 import VIDEOS2
OP.set_channel("Mialinhcute")
cfg = VIDEOS2["meme"]
video = os.path.abspath("output/Mialinhcute_v2_meme.mp4")
title = cfg["title"]
desc = cfg["desc"] + chr(10) + chr(10) + "#gacha #meme #funny #shorts #viral #relatable"
tags = cfg["tags"]
topic = "chMialinhcute_v2_meme_" + time.strftime("%Y%m%d_%H%M%S")
r = OP.publish(video, title, description=desc, tags=tags, privacy="public", topic=topic, force=True)
print(json.dumps(r, ensure_ascii=False, indent=2, default=str))