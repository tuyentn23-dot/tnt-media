import os, sys, subprocess
os.environ['IMAGEIO_FFMPEG_EXE'] = os.path.abspath(os.path.join('tools', 'ffmpeg.exe'))
sys.path.insert(0, os.path.abspath('ops'))
sys.path.insert(0, 'ops')
import importlib
gf = importlib.import_module('gacha_anime_final')
import numpy as np
from moviepy.video.VideoClip import VideoClip
DUR = 20.0
FPS = 8
N = int(DUR * FPS)
print('precompute', N, 'frames')
cache = []
for i in range(N):
	t = i * (DUR / N)
	cache.append(np.array(gf.render_frame(gf.PALETTES[0], t, seed=7)))
print('cached', len(cache))
def mk(t):
	idx = min(N - 1, int(t * FPS))
	return cache[idx]
out_video = os.path.abspath(os.path.join('output', 'CHECK', 'gacha_silent.mp4'))
os.makedirs(os.path.dirname(out_video), exist_ok=True)
clip = VideoClip(mk)
clip = clip.set_duration(DUR) if hasattr(clip, 'set_duration') else clip.with_duration(DUR)
clip = clip.set_fps(FPS) if hasattr(clip, 'set_fps') else clip.with_fps(FPS)
clip.write_videofile(out_video, fps=FPS, codec='libx264', preset='ultrafast', audio=False, logger=None)
print('silent video:', os.path.getsize(out_video))
FFMPEG = os.path.abspath(os.path.join('tools', 'ffmpeg.exe'))
music = 'assets/music_clips/clip_0_0.mp3'
final = os.path.abspath(os.path.join('output', 'CHECK', 'gacha_clip.mp4'))
cmd = [FFMPEG, '-y', '-i', out_video, '-i', music, '-c:v', 'copy', '-c:a', 'aac', '-b:a', '192k', '-shortest', final]
r = subprocess.run(cmd, capture_output=True, text=True)
print('ffmpeg rc:', r.returncode)
if r.returncode != 0:
	print(r.stderr[-500:])
print('final:', os.path.getsize(final) if os.path.exists(final) else 0)
print('DONE')