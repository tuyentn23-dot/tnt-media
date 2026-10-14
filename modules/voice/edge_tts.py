"""Edge TTS voice - Vietnamese premium voices (patched endpoint 2026-10-14)."""
from __future__ import annotations
import os, asyncio
from .base import BaseVoice

# Patch endpoint moi cua Microsoft (host cu speech.platform.bing.com bi chan tu 10-10-2026)
# Ref: rany2/edge-tts #490, readest #6722, sokuji #622
NEW_HOST = 'api.msedgeservices.com/tts/cognitiveservices/websocket/v1'
NEW_VOICE_HOST = 'api.msedgeservices.com/tts/cognitiveservices/voices/list'


def _patch_edge_tts_endpoint():
	try:
		from edge_tts import constants as _c
		token = _c.TRUSTED_CLIENT_TOKEN
		new_wss = 'wss://' + NEW_HOST + '?Ocp-Apim-Subscription-Key=' + token
		new_voice = 'https://' + NEW_VOICE_HOST + '?Ocp-Apim-Subscription-Key=' + token
		if getattr(_c, 'WSS_URL', '') != new_wss:
			_c.WSS_URL = new_wss
			_c.VOICE_LIST = new_voice
			# communicate.py dung 'from .constants import WSS_URL' -> phai patch rieng
			try:
				from edge_tts import communicate as _cm
				_cm.WSS_URL = new_wss
			except Exception:
				pass
			try:
				from edge_tts import voices as _vc
				if hasattr(_vc, 'VOICE_LIST'):
					_vc.VOICE_LIST = new_voice
			except Exception:
				pass
		# Patch headers: doi Authority + Origin
		try:
			_c.WSS_HEADERS['Origin'] = 'chrome-extension://jdiccldimpdaibmpdkjnbmckianbfold'
			h = _c.VOICE_HEADERS
			h['Authority'] = 'api.msedgeservices.com'
		except Exception:
			pass
	except Exception:
		pass


_patch_edge_tts_endpoint()

# 6 giong chuan (nam/nu x cham/nhanh + tu nhien + em be)
NEW_VOICES = {
	'nu_cham': ('female_north', '-20%', '+0Hz'),
	'nu_nhanh': ('female_north', '+25%', '+0Hz'),
	'nam_cham': ('male_north', '-20%', '+0Hz'),
	'nam_nhanh': ('male_north', '+25%', '+0Hz'),
	'tu_nhien': ('female_north', '+0%', '+0Hz'),
	'em_be': ('female_north', '+15%', '+60Hz'),
}

VI_VOICES = {
	'female_north': 'vi-VN-HoaiMyNeural',
	'male_north': 'vi-VN-NamMinhNeural',
	'female_multilingual': 'en-US-AvaMultilingualNeural',
	'female_emma': 'en-US-EmmaMultilingualNeural',
	'female_jenny': 'en-US-JennyMultilingualNeural',
	'male_andrew': 'en-US-AndrewMultilingualNeural',
}

PRESETS = {
	'default': {'rate': '+0%', 'pitch': '+0Hz', 'volume': '+0%'},
	'cheerful': {'rate': '+15%', 'pitch': '+30Hz', 'volume': '+5%'},
	'sad': {'rate': '-15%', 'pitch': '-20Hz', 'volume': '+0%'},
	'excited': {'rate': '+25%', 'pitch': '+40Hz', 'volume': '+8%'},
	'calm': {'rate': '-10%', 'pitch': '-10Hz', 'volume': '-5%'},
	'narrator': {'rate': '-5%', 'pitch': '+0Hz', 'volume': '+0%'},
	'kids': {'rate': '+10%', 'pitch': '+50Hz', 'volume': '+5%'},
	'news': {'rate': '+8%', 'pitch': '-5Hz', 'volume': '+3%'},
}


def list_voices():
	return list(NEW_VOICES.keys()) + list(VI_VOICES.keys())


def list_presets():
	return list(PRESETS.keys())


def resolve_voice(name):
	if not name:
		return VI_VOICES['female_north']
	if name in VI_VOICES:
		return VI_VOICES[name]
	if 'Neural' in str(name):
		return str(name)
	return VI_VOICES['female_north']

def resolve_new_voice_params(name):
	if name in NEW_VOICES:
		v, r, p = NEW_VOICES[name]
		return (VI_VOICES[v], r, p)
	return None


def resolve_preset(name):
	return PRESETS.get(name, PRESETS['default'])


class EdgeTTSVoice(BaseVoice):
	def __init__(self, voice='female_north', preset='default', rate=None, pitch=None, volume=None):
		np = resolve_new_voice_params(voice)
		if np and rate is None and pitch is None:
			self.voice, self.rate, self.pitch = np
			self.volume = volume if volume is not None else '+0%'
		else:
			self.voice = resolve_voice(voice)
			p = resolve_preset(preset)
			self.rate = rate if rate is not None else p['rate']
			self.pitch = pitch if pitch is not None else p['pitch']
			self.volume = volume if volume is not None else p['volume']

	def synthesize(self, text, out_path):
		if not text:
			return ''
		d = os.path.dirname(out_path)
		if d:
			os.makedirs(d, exist_ok=True)
		try:
			_patch_edge_tts_endpoint()
			import edge_tts
			async def _run():
				c = edge_tts.Communicate(text, self.voice, rate=self.rate, pitch=self.pitch, volume=self.volume)
				await c.save(out_path)
			asyncio.run(_run())
		except Exception:
			pass
		return out_path
