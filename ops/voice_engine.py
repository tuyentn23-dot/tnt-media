# voice_engine.py - edge-tts voices + presets (fully flat, no nested blocks)
import os, sys
CAND = [os.environ.get('TNT_MEDIA_ROOT'), os.getcwd()] + list(sys.path)
ROOT = next((p for p in CAND if p and os.path.isdir(os.path.join(p, 'tools'))), os.getcwd())
FFMPEG = os.path.join(ROOT, 'tools', 'ffmpeg.exe')

VI_VOICES = {
	'HoaiMy': 'vi-VN-HoaiMyNeural',
	'NamMinh': 'vi-VN-NamMinhNeural',
	'HoaiMyNeural': 'vi-VN-HoaiMyNeural',
	'NamMinhNeural': 'vi-VN-NamMinhNeural',
	'Ava': 'en-US-AvaMultilingualNeural',
	'Emma': 'en-US-EmmaMultilingualNeural',
	'Brian': 'en-US-BrianMultilingualNeural',

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
 'female_cute': {'rate': '+6%', 'pitch': '+8Hz', 'volume': '+6%'},
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

def split_sentences(text):
	t = (text or '').strip()
	if not t: return []
	raw = t.replace('. ', '|').replace('! ', '|').replace('? ', '|')
	out = [s.strip() for s in raw.split('|') if s.strip()]
	return out or [t]

def tts(text, out, voice='female_north', preset='story', rate=None, pitch=None, volume=None, pause_ms=180):
	import asyncio, edge_tts, subprocess, os, tempfile
	vid = VI_VOICES.get(voice, VI_VOICES['female_north'])
	pr = PRESETS.get(preset, PRESETS['story'])
	rate = rate or pr.get('rate', '+0%')
	pitch = pitch or pr.get('pitch', '+0Hz')
	volume = volume or pr.get('volume', '+0%')
	sents = split_sentences(text)
	def sync(coro):
		try:
			loop = asyncio.get_running_loop()
		except RuntimeError:
			loop = None
		if loop and loop.is_running():
			import concurrent.futures as cf
			with cf.ThreadPoolExecutor(1) as ex:
				return ex.submit(lambda: asyncio.run(coro)).result()
		return asyncio.run(coro)
	if len(sents) <= 1:
		async def one():
			c = edge_tts.Communicate(text, vid, rate=rate, pitch=pitch, volume=volume)
			await c.save(out)
		sync(one())
		return out
	tmp = tempfile.mkdtemp(prefix='ttsparts')
	parts = []
	for i, s in enumerate(sents):
		p = os.path.join(tmp, 'p%03d.mp3' % i)
		async def mk(ss, pp):
			c = edge_tts.Communicate(ss, vid, rate=rate, pitch=pitch, volume=volume)
			await c.save(pp)
		sync(mk(s, p))
		parts.append(p)
	sil = os.path.join(tmp, 'sil.mp3')
	if os.path.exists(FFMPEG):
		subprocess.run([FFMPEG, '-y', '-f', 'lavfi', '-i', 'anullsrc=r=24000:cl=mono', '-t', str(pause_ms/1000.0), '-q:a', '9', '-acodec', 'libmp3lame', sil], capture_output=True)
	concat = []
	for i, p in enumerate(parts):
		concat.append(p)
		if i < len(parts)-1 and os.path.exists(sil):
			concat.append(sil)
	lst = os.path.join(tmp, 'list.txt')
	with open(lst, 'w', encoding='utf-8') as f:
		for p in concat:
			f.write('file ' + chr(39) + p.replace(chr(92), chr(47)) + chr(39) + chr(10))
	if os.path.exists(FFMPEG):
		subprocess.run([FFMPEG, '-y', '-f', 'concat', '-safe', '0', '-i', lst, '-c', 'copy', out], capture_output=True)
	else:
		import shutil
		shutil.copy(parts[0], out)
	return out
