import os, sys, json, time
sys.stdout.reconfigure(encoding='utf-8', errors='replace')
sys.path.insert(0, os.getcwd())
from ops import os_publish as OP
OP.set_channel('Mialinhcute')
video = os.path.abspath('output/Mialinhcute_anime_pika.mp4')
title = 'Pikachu có thực sự là chuột? #shorts'
desc = 'Pikachu có thực sự là chuột? Bí mật ít ai biết về linh vật nổi tiếng nhất thế giới!' + chr(10) + chr(10) + '#pikachu #pokemon #anime #shorts #viral #cute'
tags = ['pikachu', 'pokemon', 'anime', 'shorts', 'viral', 'cute', 'facts']
topic = 'chMialinhcute_anime_pokemon_' + time.strftime('%Y%m%d_%H%M%S')
r = OP.publish(video, title, description=desc, tags=tags, privacy='public', topic=topic, force=True)
print(json.dumps(r, ensure_ascii=False, indent=2, default=str))