import os, sys, json, time
sys.stdout.reconfigure(encoding='utf-8', errors='replace')
sys.path.insert(0, os.getcwd())
from ops import os_publish as OP
OP.set_channel('Mialinhcute')
print('active:', OP.active_channel())
video = os.path.abspath('output/Mialinhcute_gacha_ai.mp4')
title = 'Crush của tôi không biết tôi tồn tại (Anime AI) #shorts'
desc = 'Anime AI - Crush của tôi không biết tôi tồn tại' + chr(10) + chr(10) + '#anime #gacha #shorts #viral #ai #cute'
tags = ['anime', 'gacha', 'shorts', 'viral', 'ai', 'cute', 'mia linh cute']
topic = 'chMialinhcute_gacha_ai_' + time.strftime('%Y%m%d_%H%M%S')
print('title:', title)
r = OP.publish(video, title, description=desc, tags=tags, privacy='public', topic=topic, force=True)
print(json.dumps(r, ensure_ascii=False, indent=2, default=str))