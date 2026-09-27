import sys, os, json
os.chdir('D:/TNT_AI/venture_foundry/media')
sys.path.insert(0, 'D:/TNT_AI/venture_foundry/media')
from ops import ffmpeg_render as FR
d = json.load(open('memory/content_db.json', encoding='utf-8'))
it = dict(d['facts'][10])
it['id'] = 'freshup1'
it['search_query'] = 'underwater ocean deep blue'
r = FR.render(it, 'output/v_freshup1.mp4', seed=11, scenes=5)
print('DONE', r)
