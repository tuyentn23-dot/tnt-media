import os, sys, traceback
sys.path.insert(0, os.getcwd())
os.environ['IMAGEIO_FFMPEG_EXE'] = os.path.abspath('tools/ffmpeg.exe')
import numpy as np
from ops.compat import _editor as E
ColorClip = E()[5]
VideoClip = E()[0]
b = ColorClip((720, 1280), color=(8, 10, 25), duration=4)
b = b.cropped(width=720, x_center=b.w / 2)
b = b.subclipped(0, 4)
b = b.cropped(width=720, height=1280, x_center=b.w / 2, y_center=b.h / 2)
print('b type', type(b))
print('b.get_frame', b.get_frame)
getf = b.get_frame
print('direct call:', getf(0.0).shape)
overlay = np.zeros((1280, 720, 4), dtype=np.uint8)
def mk(get, t):
	fr = get(t)
	return fr.astype('uint8')
func = lambda t: mk(b.get_frame, t)
print('lambda created, type:', type(func))
try:
	v = VideoClip(func, duration=4)
	print('VideoClip OK', type(v))
except Exception:
	traceback.print_exc()
