# tool: tnt-analyze
# -- coding: utf-8 --
# modules/analyze/video_analyzer.py - Phan tich video (scene + quality + vision)
import os, sys
U = chr(95)
FKEY = U + U + 'file' + U + U
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(globals()[FKEY]))))
sys.path.insert(0, ROOT)

MODULE = {
	'tool': 'tnt-analyze',
	'name': 'analyze.video_analyzer',
	'version': '1.0.0',
	'interface': 'analyze(path, output_dir=None, use_vision=False) -> dict',
	'deps': ['ops.scene_reader', 'ops.video_reader']
}


def log(m):
	try:
		print('[analyze] ' + str(m), flush=True)
	except Exception:
		pass


def quick_check(path):
	from ops import video_reader as vr
	return vr.read_video(path, n_frames=6, use_vision=False)


def analyze(path, output_dir=None, use_vision=False):
	from ops import video_analyzer as va
	return va.analyze_video(path, output=output_dir, use_vision=use_vision)
