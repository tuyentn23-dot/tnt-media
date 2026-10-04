# -- coding: utf-8 --
# modules/render/short.py - Render short (alias cua render.video; kind 'render.short')
import os, sys
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, ROOT)

MODULE = {
	'name': 'render.short',
	'version': '1.0.0',
	'interface': 'render(item, out, style) -> path',
	'config_schema': {'style': 'dict'},
	'deps': ['ops.ffmpeg_render'],
	'health': True,
}


def render(item, out, style=None):
	from ops import ffmpeg_render
	return ffmpeg_render.render(item, out, style)
