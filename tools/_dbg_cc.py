import os, sys
sys.path.insert(0, os.getcwd())
os.environ['IMAGEIO_FFMPEG_EXE'] = os.path.abspath('tools/ffmpeg.exe')
import ops.compat as m
E = getattr(m, '_editor')
C = E()[5]
c = C((720, 1280), color=(8, 10, 25), duration=3)
print('methods:')
for x in dir(c):
	xl = x.lower()
	if 'crop' in xl or 'resiz' in xl or 'effect' in xl or 'sub' in xl or 'with_' in xl:
		print(' ', x)