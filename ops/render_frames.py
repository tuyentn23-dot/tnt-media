import os, sys
sys.path.insert(0, os.path.abspath('ops'))
sys.path.insert(0, 'ops')
import importlib
gf = importlib.import_module('gacha_anime_final')
OUT = os.path.abspath(os.path.join('output', 'frames_tmp'))
os.makedirs(OUT, exist_ok=True)
DUR = 20.0
FPS = 6
N = int(DUR * FPS)
print('render', N, 'frames')
for i in range(N):
	t = i * (DUR / N)
	im = gf.render_frame(gf.PALETTES[0], t, seed=7)
	im.save(os.path.join(OUT, 'f%04d.png' % i))
	if i % 10 == 0:
		print('frame', i)
print('DONE frames')