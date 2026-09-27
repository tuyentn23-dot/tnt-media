import sys, os, json
sys.stdout.reconfigure(encoding="utf-8")
os.chdir('D:/TNT_AI/venture_foundry/media')
sys.path.insert(0, 'D:/TNT_AI/venture_foundry/media')
import ops.channel_render as CR
d = json.load(open('channels/Mialinhcute/content_db.json', encoding='utf-8'))
it = dict(d['cute_animals'][0]); it['id'] = 'demo_mia'
r = CR.render_for('Mialinhcute', it, 'output/DEMO_MIA.mp4', scenes=8)
print('MIA', isinstance(r,str), os.path.getsize(r) if isinstance(r,str) else r)
d2 = json.load(open('channels/vilevi5676/content_db.json', encoding='utf-8'))
it2 = dict(d2['food'][0]); it2['id'] = 'demo_vile'
r2 = CR.render_for('vilevi5676', it2, 'output/DEMO_VILE.mp4', scenes=8)
print('VILE', isinstance(r2,str), os.path.getsize(r2) if isinstance(r2,str) else r2)
