import os, sys, time
sys.stdout.reconfigure(encoding='utf-8', errors='replace')
sys.path.insert(0, os.getcwd())
from ops import gacha_anime_render as GAR
t0 = time.time()
out = os.path.abspath(os.path.join('output', 'anim_test.mp4'))
GAR.make_anime(out, dur=4.0, seed=42, pal_idx=1, fps=6)
print('elapsed:', round(time.time() - t0, 1), 's')
print('size:', os.path.getsize(out))