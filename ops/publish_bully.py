import os, sys, json, time
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
sys.path.insert(0, os.getcwd())
from ops import os_publish as OP
from ops.gacha_viral_pack import VIDEOS
OP.set_channel("Mialinhcute")
cfg = VIDEOS["bully"]
video = os.path.abspath("output/Mialinhcute_gacha_bully.mp4")
title = cfg["title"]
desc = cfg["desc"] + chr(10) + chr(10) + "#gacha #gachaclub #pov #shorts #viral #bully #glowup"
tags = cfg["tags"]
topic = "chMialinhcute_gacha_bully_" + time.strftime("%Y%m%d_%H%M%S")
print("title:", title)
r = OP.publish(video, title, description=desc, tags=tags, privacy="public", topic=topic, force=True)
print(json.dumps(r, ensure_ascii=False, indent=2, default=str))