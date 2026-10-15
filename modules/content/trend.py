# tool: content-trend
# -- coding: utf-8 --
# modules/content/trend.py - Phan tich xu huong
import os, sys
U = chr(95)
FKEY = U + U + 'file' + U + U
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(globals()[FKEY]))))
sys.path.insert(0, ROOT)

MODULE = {
	'tool': 'content-trend',
	'name': 'content.trend',
	'version': '1.0.0',
	'interface': 'run() -> dict',
	'deps': ['ops.trend_analyzer']
}


def run():
	from ops import trend_analyzer as ta
	return ta.run()
