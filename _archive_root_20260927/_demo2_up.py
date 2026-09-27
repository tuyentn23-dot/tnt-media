import sys, os, time
sys.stdout.reconfigure(encoding="utf-8")
os.chdir('D:/TNT_AI/venture_foundry/media')
sys.path.insert(0, 'D:/TNT_AI/venture_foundry/media')
from ops import os_publish as OP
OP.set_channel('Mialinhcute')
r1 = OP.publish('output/DEMO2_MIA.mp4', '[DEMO2] Video that motion - Mia #shorts', 'demo video motion', tags=['shorts'], privacy='unlisted', topic='demo2_mia_'+str(int(time.time())), force=True)
print('MIA', r1.get('url') or r1.get('error'))
OP.set_channel('vilevi5676')
r2 = OP.publish('output/DEMO2_VILE.mp4', '[DEMO2] Video that motion - ViLe #shorts', 'demo video motion', tags=['shorts'], privacy='unlisted', topic='demo2_vile_'+str(int(time.time())), force=True)
print('VILE', r2.get('url') or r2.get('error'))
