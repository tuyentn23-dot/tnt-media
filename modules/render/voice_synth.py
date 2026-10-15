# tool: edge-tts
# -- coding: utf-8 --
# modules/render/voice_synth.py v1.1.0
# Sinh giong doc (edge-tts) + word timings, co retry + fallback chia timing.
import os, sys, asyncio, tempfile
U = chr(95)
FKEY = U + U + 'file' + U + U
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(globals()[FKEY]))))
sys.path.insert(0, ROOT)

MODULE = {
	'tool': 'edge-tts',
	'name': 'render.voice_synth',
	'version': '1.1.0',
	'interface': 'synth_words(text, out_mp3, voice, rate, pitch) -> dict',
	'deps': ['edge_tts']
}

VI_VOICES = {
	'female_north': 'vi-VN-HoaiMyNeural',
	'male_north': 'vi-VN-NamMinhNeural',
	'female_multi': 'en-US-AvaMultilingualNeural',
}
FFMPEG = os.path.join(ROOT, 'tools', 'ffmpeg.exe')


def log(m):
	try:
		print('[voice_synth] ' + str(m), flush=True)
	except Exception:
		pass


def resolve_voice(voice):
	if not voice:
		return VI_VOICES['female_north']
	if voice in VI_VOICES:
		return VI_VOICES[voice]
	if 'Neural' in str(voice):
		return str(voice)
	return VI_VOICES['female_north']


def _run_sync(coro):
	try:
		loop = asyncio.get_running_loop()
	except RuntimeError:
		loop = None
	if loop and loop.is_running():
		import concurrent.futures as cf
		with cf.ThreadPoolExecutor(1) as ex:
			return ex.submit(lambda: asyncio.run(coro)).result()
	return asyncio.run(coro)


def audio_dur(path):
	import re, subprocess
	try:
		r = subprocess.run([FFMPEG, '-i', path, '-hide_banner'], capture_output=True, text=True, timeout=30, creationflags=0x08000000)
		m = re.search('Duration: (\d+):(\d+):(\d+\.\d+)', r.stderr)
		if m:
			return int(m.group(1)) * 3600 + int(m.group(2)) * 60 + float(m.group(3))
	except Exception:
		pass
	return 0.0


def _split_words(text):
	return [w for w in str(text or '').split() if w]


def _proportional_words(text, dur):
	ws = _split_words(text)
	if not ws or dur <= 0:
		return []
	tot = sum(len(w) for w in ws) or len(ws)
	t = 0.0
	segs = []
	for w in ws:
		d = dur * (len(w) / tot)
		segs.append([round(t, 3), round(t + d, 3), w])
		t += d
	return segs



def proportional_words_by_sentence(sentences, total_dur, gap=0.15):
	# Chia timing THEO TUNG CAU - dam bao khong tron ranh gioi cau
	# sentences: list[str] da duoc tach san
	# total_dur: tong thoi luong audio (giay)
	if not sentences or total_dur <= 0:
		return []
	# Tinh tong ky tu (khong tinh khoang trang thua) de phan bo thoi gian
	lens = [max(1, len(str(s).strip())) for s in sentences]
	total_len = sum(lens)
	# Tru gap giua cac cau
	n_gaps = max(0, len(sentences) - 1)
	gap_total = gap * n_gaps
	speech_dur = max(0.1, total_dur - gap_total)
	segs = []
	t = 0.0
	for i, s in enumerate(sentences):
		text = str(s).strip()
		if not text:
			continue
		# Doan nay chiem bao nhieu thoi luong
		d_seg = speech_dur * (lens[i] / total_len)
		sent_start = t
		sent_end = t + d_seg
		# Chia tung tu trong cau
		words = text.split()
		if words:
			w_total = sum(max(1, len(w)) for w in words)
			wt = sent_start
			for w in words:
				wd = d_seg * (max(1, len(w)) / w_total)
				segs.append([round(wt, 3), round(wt + wd, 3), w])
				wt += wd
		t = sent_end + gap
	return segs

def _synth_stream(txt, vid, out_mp3, rate, pitch):
	import edge_tts
	words = []
	async def go():
		c = edge_tts.Communicate(txt, vid, rate=rate, pitch=pitch)
		with open(out_mp3, 'wb') as f:
			async for chunk in c.stream():
				if chunk.get('type') == 'audio':
					f.write(chunk['data'])
				elif chunk.get('type') == 'WordBoundary':
					off = chunk.get('offset', 0) / 10000000.0
					dur = chunk.get('duration', 0) / 10000000.0
					words.append([round(off, 3), round(off + dur, 3), chunk.get('text', '')])
	_run_sync(go())
	return words


def _synth_save(txt, vid, out_mp3, rate, pitch):
	import edge_tts
	async def go():
		c = edge_tts.Communicate(txt, vid, rate=rate, pitch=pitch)
		await c.save(out_mp3)
	_run_sync(go())


def synth_words(text, out_mp3, voice=None, rate=None, pitch=None, volume=None, preset='default', attempts=3):
	import time
	try:
		from modules.voice import edge_tts as _ev
		p = _ev.resolve_preset(preset)
		if rate is None:
			rate = p['rate']
		if pitch is None:
			pitch = p['pitch']
		if volume is None:
			volume = p['volume']
	except Exception:
		if rate is None:
			rate = '+0%'
		if pitch is None:
			pitch = '+0Hz'
		if volume is None:
			volume = '+0%'
	vid = resolve_voice(voice)
	txt = (text or '').strip()
	if not txt:
		return {'ok': False, 'error': 'empty text'}
	d = os.path.dirname(os.path.abspath(out_mp3))
	os.makedirs(d, exist_ok=True)
	last = None
	for a in range(1, attempts + 1):
		try:
			if os.path.exists(out_mp3):
				os.remove(out_mp3)
			words = _synth_stream(txt, vid, out_mp3, rate, pitch)
			sz = os.path.getsize(out_mp3) if os.path.exists(out_mp3) else 0
			if sz > 0:
				if not words:
					words = _proportional_words(txt, audio_dur(out_mp3))
				return {'ok': True, 'path': out_mp3, 'size': sz, 'words': words, 'voice': vid, 'mode': 'stream'}
			last = 'empty stream output'
		except Exception as e:
			last = str(e)[:160]
		try:
			if os.path.exists(out_mp3):
				os.remove(out_mp3)
			_synth_save(txt, vid, out_mp3, rate, pitch)
			sz = os.path.getsize(out_mp3) if os.path.exists(out_mp3) else 0
			if sz > 0:
				words = _proportional_words(txt, audio_dur(out_mp3))
				return {'ok': True, 'path': out_mp3, 'size': sz, 'words': words, 'voice': vid, 'mode': 'save+proportional'}
			last = 'empty save output'
		except Exception as e:
			last = str(e)[:160]
		time.sleep(1.2 * a)
	return {'ok': False, 'error': 'voice synth failed: ' + str(last)}
