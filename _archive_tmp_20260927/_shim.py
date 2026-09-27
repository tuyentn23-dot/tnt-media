import os,sys
sys.path.insert(0,os.getcwd())
import ops.compat
from moviepy.editor import ImageClip
print('with_duration', hasattr(ImageClip,'with_duration'))
print('with_position', hasattr(ImageClip,'with_position'))
