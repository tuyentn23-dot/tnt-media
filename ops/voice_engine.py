# voice_engine.py - edge-tts voices + presets (fully flat, no nested blocks)
import os, sys
CAND = [os.environ.get('TNT_MEDIA_ROOT'), os.getcwd()] + list(sys.path)
ROOT = next((p for p in CAND if p and os.path.isdir(os.path.join(p, 'tools'))), os.getcwd())
FFMPEG = os.path.join(ROOT, 'tools', 'ffmpeg.exe')

VI_VOICES = {
	'female_north': 'vi-VN-HoaiMyNeural',
	'male_north': 'vi-VN-NamMinhNeural',
	'female_ava': 'en-US-AvaMultilingualNeural',
	'female_emma': 'en-US-EmmaMultilingualNeural',
	'male_brian': 'en-US-BrianMultilingualNeural',
	'female_multi': 'en-US-AvaMultilingualNeural',
}

PRESETS = {
 'hype': {'rate': '+12%', 'pitch': '+2Hz', 'volume': '+8%'},
 'story': {'rate': '+4%', 'pitch': '+0Hz', 'volume': '+0%'},
 'calm': {'rate': '-4%', 'pitch': '-2Hz', 'volume': '+0%'},
 'cute': {'rate': '+6%', 'pitch': '+8Hz', 'volume': '+6%'},
}

def _run(coro):
	import asyncio
	try:
		loop = asyncio.get_running_loop()
	except RuntimeError:
		loop = None
	if loop and loop.is_running():
		import concurrent.futures as cf
		with cf.ThreadPoolExecutor(1) as ex:
			return ex.submit(lambda: asyncio.run(coro)).result()
	return asyncio.run(coro)
