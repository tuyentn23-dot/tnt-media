import sys, os
sys.path.insert(0, 'ops')
import importlib
gf = importlib.import_module('gacha_anime_final')
os.environ['IMAGEIO_FFMPEG_EXE'] = os.path.abspath(os.path.join('tools', 'ffmpeg.exe'))
from moviepy.video.VideoClip import VideoClip
import numpy as np
# precompute 16 frame voi t khac nhau
N = 16
cache = []
for i in range(N):
	t = i * 0.15
	cache.append(np.array(gf.render_frame(gf.PALETTES[0], t, seed=7)))
print('precomputed', N)
def mk(t):
	idx = int(t / 0.15) % N
	return cache[idx]
out = os.path.abspath(os.path.join('output', 'CHECK', 'anime_preview.mp4'))
os.makedirs(os.path.dirname(out), exist_ok=True)
clip = VideoClip(mk)
clip = clip.set_duration(2.0) if hasattr(clip, 'set_duration') else clip.with_duration(2.0)
clip = clip.set_fps(8) if hasattr(clip, 'set_fps') else clip.with_fps(8)
clip.write_videofile(out, fps=8, codec='libx264', preset='ultrafast', audio=False, logger=None)
print('size:', os.path.getsize(out))
print('DONE')