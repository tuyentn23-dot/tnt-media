import os, sys
os.chdir('D:/TNT_AI/venture_foundry/media')
sys.path.insert(0, 'D:/TNT_AI/venture_foundry/media')
import json
from ops import mia_producer as MP
cd = json.load(open('channels/Mialinhcute/content_db.json', encoding='utf-8'))
targets = {'anime_onepiece', 'meme_funny_cat_1'}
allit = [(k, it) for k in cd for it in cd[k]]
sel = [(k,it) for k,it in allit if it.get('id') in targets]
rows = [MP.produce(k, it, live=True) for k,it in sel]
zz = [print(r) for r in rows]
print('DONE')
