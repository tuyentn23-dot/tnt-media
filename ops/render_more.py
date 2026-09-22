import os, sys
sys.path.insert(0, os.path.abspath('ops'))
sys.path.insert(0, 'ops')
import importlib
gf = importlib.import_module('gacha_anime_final')
OUT = os.path.abspath(os.path.join('output', 'frames_tmp'))
DUR = 20.0
FPS = 6
N = int(DUR * FPS)
start = 0
for i in range(N):
	fp = os.path.join(OUT, 'f%04d.png' % i)
	if os.path.exists(fp):
		start = i + 1
print('resume from', start)
import time
t0 = time.time()
for i in range(start, N):
	t = i * (DUR / N)
	im = gf.render_frame(gf.PALETTES[0], t, seed=7)
	im.save(os.path.join(OUT, 'f%04d.png' % i))
	if (i - start) % 10 == 0:
		print('frame', i, 'elapsed', round(time.time() - t0, 1))
	if time.time() - t0 > 45:
		print('time budget hit, stop at', i)
		break
print('DONE')