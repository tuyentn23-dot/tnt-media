# -- coding: utf-8 --
# modules/voice/tts.py - Wrapper voice_engine
import os, sys
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, ROOT)
MODULE = {
	'name': 'voice.tts',
	'version': '1.0.0',
	'interface': 'tts(text, out, voice) -> path',
	'config_schema': { 'voice': 'str' },
	'deps': ['ops.voice_engine']
}
def tts(text, out, voice=None):
	from ops import voice_engine as ve
	if hasattr(ve, 'tts'):
		return ve.tts(text, out, voice=voice)
	from ops import content_video5 as cv5
	cv5.tts(text, out)
	return out
def health():
	try:
		from ops import voice_engine
		return True
	except Exception:
		return False
