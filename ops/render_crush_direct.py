import os, sys, time
sys.stdout.reconfigure(encoding='utf-8', errors='replace')
sys.path.insert(0, os.getcwd())
from ops import channel_render as CR
import json
d = json.load(open('channels/Mialinhcute/content_db.json', encoding='utf-8'))
item = [x for x in d['gacha'] if x['id'] == 'gacha_crush'][0]
out = os.path.abspath('output/Mialinhcute_gacha_crush.mp4')
print('start render...')
t0 = time.time()
r = CR.render_for('Mialinhcute', dict(item), out, scenes=5)
print('elapsed', round(time.time() - t0, 1))
print('result', r)
print('size', os.path.getsize(out) if os.path.exists(out) else 0)