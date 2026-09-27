# -- coding: utf-8 --
# modules/render/video.py - Render wrapper dung ffmpeg_render (P0 upgrade)
import os, sys
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, ROOT)

MODULE = {
	'name': 'render.video',
	'version': '2.0.0',
	'interface': 'render(item, out, style) -> path',
	'config_schema': {'style': 'dict'},
	'deps': ['ops.ffmpeg_render']
}


def render(item, out, style=None):
	from ops import ffmpeg_render as fr
	style = style or {}
	voice = style.get('voice', 'female_north')
	preset = style.get('preset', style.get('voice_preset', 'cute'))
	music = style.get('music_mood') or style.get('music')
	seed = style.get('seed')
	try:
		r = fr.render(item, out, voice=voice, preset=preset, seed=seed, music=music)
	except TypeError:
		r = fr.render(item, out, voice=voice, preset=preset, seed=seed)
	return out


def health():
	try:
		from ops import ffmpeg_render
		return True
	except Exception:
		return False
