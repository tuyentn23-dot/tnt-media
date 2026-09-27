import os, sys
os.chdir('D:/TNT_AI/venture_foundry/media')
sys.path.insert(0, 'D:/TNT_AI/venture_foundry/media')
from ops import channel_producer as CP
rows = CP.run_many('vilevi5676', limit=6, live=True)
zz = [print(r) for r in rows]
print('DONE')
