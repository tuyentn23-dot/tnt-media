import os, sys
sys.path.insert(0, os.getcwd())
U = chr(95)
from ops.compat import get_video_clip
V = get_video_clip()
f = 'library/anime/clip36897756.mp4'
try:
	c = V(f)
	print('Clip OK:', c.size, c.duration)
	fr = c.get_frame(0)
	print('Frame shape:', fr.shape, fr.dtype)
except Exception as e:
	import traceback
	traceback.print_exc()
