# -- coding: utf-8 --
# modules/render/music.py - Wrapper music_mixer
import os, sys
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, ROOT)
MODULE = {
	'name': 'render.music',
	'version': '1.0.0',
	'interface': 'mix(voice, music, out) -> path',
	'config_schema': { 'topic': 'str' },
	'deps': ['ops.music_mixer']
}
def mix(voice, music, out):
	from ops import music_mixer as mm
	mm.mix(voice, music, out)
	return out
def pick(topic=''):
	from ops import music_mixer as mm
	return mm.pick_music(topic)
def health():
	try:
		from ops import music_mixer
		return True
	except Exception:
		return False
