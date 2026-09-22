import os, sys, json, time
sys.stdout.reconfigure(encoding='utf-8', errors='replace')
sys.path.insert(0, os.getcwd())
from ops import os_publish as OP
OP.set_channel('Mialinhcute')
video = os.path.abspath('output/Mialinhcute_gacha_viral2.mp4')
title = 'POV: Cô gái mèo hồng dễ thương nhất trường #shorts'
desc = 'POV: Cô gái mèo hồng dễ thương nhất trường. Nhưng không ai biết bí mật đằng sau nụ cười!' + chr(10) + chr(10) + '#gacha #gachaclub #gachalife #shorts #viral #cute #aesthetic'
tags = ['gacha', 'gachaclub', 'gachalife', 'shorts', 'viral', 'cute', 'aesthetic', 'pov']
topic = 'chMialinhcute_gacha_viral_' + time.strftime('%Y%m%d_%H%M%S')
r = OP.publish(video, title, description=desc, tags=tags, privacy='public', topic=topic, force=True)
print(json.dumps(r, ensure_ascii=False, indent=2, default=str))