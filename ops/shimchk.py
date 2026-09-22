import os,sys
sys.path.insert(0,os.getcwd())
import ops.compat
from moviepy.Clip import Clip
print('with_duration', hasattr(Clip,'with_duration'))
print('with_position', hasattr(Clip,'with_position'))
print('with_audio', hasattr(Clip,'with_audio'))
print('with_fps', hasattr(Clip,'with_fps'))
