import os, sys, traceback
sys.path.insert(0, os.getcwd())
os.environ['IMAGEIO_FFMPEG_EXE'] = os.path.abspath('tools/ffmpeg.exe')
import numpy as np
from ops.compat import _editor as E
ColorClip = E()[5]
VideoClip = E()[0]
b = ColorClip((720, 1280), color=(8, 10, 25), duration=4)
b = b.cropped(width=720, x_center=b.w / 2)
print('after cropped1', type(b))
if b.h < 1280:
	b = b.resized(height=1280)
b = b.subclipped(0, 4)
b = b.cropped(width=720, height=1280, x_center=b.w / 2, y_center=b.h / 2)
print('after cropped2', type(b))
overlay = np.zeros((1280, 720, 4), dtype=np.uint8)
def mk(get, t):
	fr = get(t)
	return fr.astype('uint8')
try:
	v = VideoClip(lambda t: mk(b.get_frame, t), duration=4)
	print('VideoClip OK', type(v))
except Exception as e:
	print('ERR', type(e).name, str(e))
	traceback.print_exc()
