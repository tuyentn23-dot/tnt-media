import sys, os, time
sys.stdout.reconfigure(encoding="utf-8")
os.chdir('D:/TNT_AI/venture_foundry/media')
sys.path.insert(0, 'D:/TNT_AI/venture_foundry/media')
from ops import os_publish as OP
OP.set_channel('Mialinhcute')
r = OP.publish('output/GACHA_ANIME.mp4', 'Gacha anime - Crush khong biet toi ton tai #gacha #shorts', 'Cau chuyen gacha anime', tags=['gacha', 'anime', 'shorts'], privacy='public', topic='gacha_anime_'+str(int(time.time())), force=True)
print('URL', r.get('url') or r.get('error'))
