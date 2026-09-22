import os, sys
os.environ['IMAGEIO_FFMPEG_EXE'] = os.path.abspath('tools/ffmpeg.exe')
from moviepy.video.VideoClip import VideoClip
m = getattr(VideoClip, chr(109) + 'ro')()
for c in m:
	print(c)
