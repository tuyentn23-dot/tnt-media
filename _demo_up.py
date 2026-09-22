import sys, os, json, time
sys.stdout.reconfigure(encoding="utf-8")
os.chdir('D:/TNT_AI/venture_foundry/media')
sys.path.insert(0, 'D:/TNT_AI/venture_foundry/media')
from ops import os_publish as OP
OP.set_channel('Mialinhcute')
r1 = OP.publish('output/DEMO_MIA.mp4', '[DEMO] Video mau kenh Mia #shorts', 'Video demo danh gia chat luong', tags=['shorts'], privacy='unlisted', topic='demo_mia_'+str(int(time.time())), force=True)
print('MIA', r1.get('url') or r1.get('error'))
OP.set_channel('vilevi5676')
r2 = OP.publish('output/DEMO_VILE.mp4', '[DEMO] Video mau kenh ViLe Vi #shorts', 'Video demo danh gia', tags=['shorts'], privacy='unlisted', topic='demo_vile_'+str(int(time.time())), force=True)
print('VILE', r2.get('url') or r2.get('error'))
