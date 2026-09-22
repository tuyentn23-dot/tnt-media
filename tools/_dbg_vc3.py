import os, sys, inspect
os.environ['IMAGEIO_FFMPEG_EXE'] = os.path.abspath('tools/ffmpeg.exe')
from moviepy.video.VideoClip import VideoClip
src = inspect.getsource(VideoClip)
name = chr(95) + chr(95) + 'init' + chr(95) + chr(95)
i = src.find('def ' + name)
print(src[i + 700:i + 2000])
