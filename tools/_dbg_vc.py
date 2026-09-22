import os, sys, inspect
os.environ['IMAGEIO_FFMPEG_EXE'] = os.path.abspath('tools/ffmpeg.exe')
from moviepy.video.VideoClip import VideoClip
name = chr(95) + chr(95) + 'init' + chr(95) + chr(95)
fn = getattr(VideoClip, name)
print('signature:', inspect.signature(fn))
print('doc:', fn.doc)
