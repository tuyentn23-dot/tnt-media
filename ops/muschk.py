import os,sys
sys.path.insert(0,os.getcwd())
from ops.auto_publish import _music_for
for t in ['anime','roblox','cute_animals','meme','gacha','animal','food']:
    print(t, os.path.basename(str(_music_for(t))))
