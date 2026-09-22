import os, sys, traceback
sys.path.insert(0, os.getcwd())
os.environ['IMAGEIO_FFMPEG_EXE'] = os.path.abspath('tools/ffmpeg.exe')
from ops import content_video5 as cv5
item = {'id': 't', 'topic': 'naruto', 'hook': 'a', 'body': 'b', 'payoff': 'c', 'question': 'd'}
os.makedirs('output', exist_ok=True)
try:
	cv5.build(item, 'output/t.mp4')
except Exception:
	tb = traceback.format_exc()
	print(tb)
