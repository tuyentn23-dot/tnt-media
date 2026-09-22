import os, sys, traceback
os.environ['IMAGEIO_FFMPEG_EXE'] = os.path.abspath('tools/ffmpeg.exe')
from moviepy.video.VideoClip import VideoClip
import numpy as np

def mk(get, t):
	return get(t).astype('uint8')

f = lambda t: mk(None, t)
try:
	v = VideoClip(f, duration=4)
	print('OK')
except Exception:
	traceback.print_exc()
