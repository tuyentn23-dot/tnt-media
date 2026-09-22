import os, sys, traceback
sys.path.insert(0, os.getcwd())
os.environ['IMAGEIO_FFMPEG_EXE'] = os.path.abspath('tools/ffmpeg.exe')
from ops import content_video5 as cv5
item = {'id': 'test1', 'topic': 'naruto', 'hook': 'xin chao', 'body': 'day la test', 'payoff': 'ket thuc', 'question': 'ok?'}
out = os.path.join('output', 'test1.mp4')
os.makedirs('output', exist_ok=True)
try:
	cv5.build(item, out)
except Exception as e:
	print('EXC TYPE:', type(e).name)
	print('EXC MSG:', str(e))
	tb = traceback.format_exc().splitlines()
	for line in tb[-8:]:
		print(line)
