# -- coding: utf-8 --
"""TNT Media OS - art documentary long-form builder.

Famous painting + mystery narration -> ~20 min Vietnamese video:
Wikimedia image + LLM script + edge-tts voice + Ken Burns + music.
"""
import os
import sys
import io
import json
import time
import subprocess

ROOT = os.path.abspath('.')
sys.path.insert(0, ROOT)
os.environ.setdefault('IMAGEIO_FFMPEG_EXE', os.path.join(ROOT, 'tools', 'ffmpeg.exe'))

FFMPEG = os.path.join(ROOT, 'tools', 'ffmpeg.exe')
ASSETS = os.path.join(ROOT, 'projects', 'art_doc', 'assets')
OUTDIR = os.path.join(ROOT, 'output')
MUSIC = os.path.join(ROOT, 'library', 'music_bed.wav')
VOICE = 'vi-VN-HoaiMyNeural'
UA = {'User-Agent': 'TNTMedia/1.0 (art documentary)'}


def log(*a):
	sys.stdout.write(' '.join(str(x) for x in a) + chr(10))
	sys.stdout.flush()


def fetch_image(url, dest):
	import urllib.request
	os.makedirs(os.path.dirname(dest), exist_ok=True)
	req = urllib.request.Request(url, headers=UA)
	data = urllib.request.urlopen(req, timeout=90).read()
	open(dest, 'wb').write(data)
	return dest


def search_image(query, width=1280):
	import urllib.request, urllib.parse
	q = urllib.parse.quote(query)
	url = ('https://commons.wikimedia.org/w/api.php?action=query&format=json&generator=search&gsrsearch='
		+ q + '&gsrlimit=1&gsrnamespace=6&prop=imageinfo&iiprop=url&iiurlwidth=' + str(width))
	req = urllib.request.Request(url, headers=UA)
	d = json.loads(urllib.request.urlopen(req, timeout=60).read().decode('utf-8'))
	pages = (d.get('query') or {}).get('pages') or {}
	for k, v in pages.items():
		ii = (v.get('imageinfo') or [{}])[0]
		u = ii.get('thumburl') or ii.get('url')
		if u:
			return u
	return None


def _font():
	p = 'tools/font.ttf'
	if os.path.exists(p):
		return p
	return 'C:/Windows/Fonts/arialbd.ttf'


def tts_long(text, out_mp3):
	import asyncio, edge_tts
	text = (text or '').strip()
	if not text:
		raise ValueError('empty tts')
	async def _run(t, out):
		com = edge_tts.Communicate(t, VOICE)
		await com.save(out)
	def _one(t, out):
		for i in range(6):
			try:
				asyncio.run(_run(t, out))
				if os.path.exists(out) and os.path.getsize(out) > 800:
					return True
			except Exception:
				pass
			time.sleep(5)
		try:
			from gtts import gTTS
			gTTS(text=t, lang='vi').save(out)
			if os.path.exists(out) and os.path.getsize(out) > 800:
				return True
		except Exception:
			pass
		return False
	
	words = text.split()
	chunks = []
	cur = []
	for w in words:
		cur.append(w)
		if len(chr(32).join(cur)) > 500:
			chunks.append(chr(32).join(cur))
			cur = []
	if cur:
		chunks.append(chr(32).join(cur))
	parts = []
	for i, c in enumerate(chunks):
		op = out_mp3 + chr(46) + str(i) + chr(46) + 'mp3'
		if _one(c, op):
			parts.append(op)
	if not parts:
		raise RuntimeError('tts all chunks failed')
	lst = out_mp3 + chr(46) + 'txt'
	lines = ['file ' + "'" + os.path.abspath(x).replace(chr(92), chr(47)) + "'" for x in parts]
	open(lst, 'w', encoding='utf-8').write(chr(10).join(lines))
	cmd = [FFMPEG, '-y', '-hide_banner', '-f', 'concat', '-safe', '0', '-i', lst, '-c', 'copy', out_mp3]
	subprocess.run(cmd, capture_output=True, text=True, encoding='utf-8', errors='replace')
	if not os.path.exists(out_mp3) or os.path.getsize(out_mp3) < 800:
		raise RuntimeError('tts concat failed')
	return out_mp3


def ollama(prompt, model=None, timeout=600):
	import urllib.request
	model = model or os.environ.get('TNT_OLLAMA_MODEL', 'llama3.2:1b')
	url = 'http://127.0.0.1:11434/api/generate'
	payload = json.dumps({'model': model, 'prompt': prompt, 'stream': False,
		'options': {'temperature': 0.8, 'num_predict': 2048}, 'keep_alive': '30m'}).encode('utf-8')
	last = None
	for i in range(3):
		try:
			req = urllib.request.Request(url, data=payload, headers={'Content-Type': 'application/json'})
			r = json.loads(urllib.request.urlopen(req, timeout=timeout).read().decode('utf-8'))
			return (r.get('response') or '').strip()
		except Exception as e:
			last = e
		time.sleep(3)
	raise RuntimeError('ollama failed: ' + str(last))


def write_script(art, facts, sections=12):
	parts = []
	for i in range(sections):
		req = ('Viết bằng TIẾNG VIỆT phần ' + str(i + 1) + ' của kịch bản documentary về ' + art
			+ ', khoảng 400 từ, giọng bí ẩn ly kỳ. Thông tin: ' + facts
			+ '. Bắt đầu bằng một dòng tiêu đề ngắn, rồi đến nội dung. Chỉ viết phần này.')
		t = ollama(req)
		lines = [x for x in t.split(chr(10)) if x.strip()]
		if lines:
			parts.append({'heading': lines[0].strip()[:120], 'text': chr(10).join(lines[1:]).strip() or t})
	return {'title': art, 'hook': art, 'parts': parts}


def _ffprobe_dur(path):
	cmd = [FFMPEG, '-hide_banner', '-i', path, '-f', 'null', '-']
	r = subprocess.run(cmd, capture_output=True, text=True, encoding='utf-8', errors='replace')
	import re
	m = re.findall(r'time=([0-9]+):([0-9]+):([0-9]+[.][0-9]+)', r.stderr)
	if not m:
		return 0.0
	h, mm, ss = m[-1]
	return int(h) * 3600 + int(mm) * 60 + float(ss)


def render_segment(img, text, audio_mp3, out_mp4, dur, idx):
	fps = 30
	d = max(3.0, float(dur))
	frames = int(d * fps)
	zoom = 'min(zoom+0.0008,1.25)'
	vf = ('scale=1536:-2,zoompan=z=' + chr(39) + zoom + chr(39) + ':d=' + str(frames) + ':s=1280x720:fps=' + str(fps))
	font = _font()
	if font and text and text.strip():
		capfile = out_mp4 + '.txt'
		open(capfile, 'w', encoding='utf-8').write(text)
		capf_f = os.path.relpath(capfile).replace(chr(92), '/')
		vf += ',drawtext=fontfile=' + font + ':textfile=' + capf_f + ':fontcolor=white:fontsize=34:box=1:boxcolor=black@0.45:boxborderw=18:x=(w-text_w)/2:y=h-140'
	cmd = [FFMPEG, '-y', '-hide_banner', '-loop', '1', '-i', img, '-i', audio_mp3,
		'-map', '0:v:0', '-map', '1:a:0', '-vf', vf, '-t', str(d),
		'-c:v', 'libx264', '-preset', 'veryfast', '-crf', '23', '-pix_fmt', 'yuv420p',
		'-c:a', 'aac', '-b:a', '160k', '-ar', '44100', '-ac', '2', '-shortest', out_mp4]
	r = subprocess.run(cmd, capture_output=True, text=True, encoding='utf-8', errors='replace')
	if not os.path.exists(out_mp4):
		log('RENDER FAIL', out_mp4, r.stderr[-300:])
	return out_mp4


def _concat(parts, out_mp4):
	lst = os.path.join(OUTDIR, '_concat_list.txt')
	open(lst, 'w', encoding='utf-8').write(''.join("file '" + p.replace(chr(92), '/') + "'" + chr(10) for p in parts))
	cmd = [FFMPEG, '-y', '-hide_banner', '-f', 'concat', '-safe', '0', '-i', lst, '-c', 'copy', out_mp4]
	subprocess.run(cmd, capture_output=True, text=True, encoding='utf-8', errors='replace')
	return out_mp4


def add_music(video_mp4, out_mp4):
	if not os.path.exists(MUSIC):
		return video_mp4
	dur = _ffprobe_dur(video_mp4)
	if dur <= 0:
		return video_mp4
	cmd = [FFMPEG, '-y', '-hide_banner', '-i', video_mp4, '-stream_loop', '-1', '-i', MUSIC,
		'-filter_complex', '[1:a]volume=0.15,afade=t=in:st=0:d=2[m];[0:a][m]amix=inputs=2:duration=first:dropout_transition=0[a]',
		'-map', '0:v:0', '-map', '[a]', '-c:v', 'copy', '-c:a', 'aac', '-b:a', '160k', '-shortest', out_mp4]
	subprocess.run(cmd, capture_output=True, text=True, encoding='utf-8', errors='replace')
	return out_mp4 if os.path.exists(out_mp4) else video_mp4


def build_art_video(art, facts, images, slug, sections=12):
	os.makedirs(OUTDIR, exist_ok=True)
	tmp = os.path.join(OUTDIR, 'artseg' + slug)
	os.makedirs(tmp, exist_ok=True)
	log('[' + slug + '] writing script...')
	sc = write_script(art, facts, sections=sections)
	if not sc or not sc.get('parts'):
		raise RuntimeError('script generation failed for ' + art)
	parts = sc['parts']
	log('[' + slug + '] script parts:', len(parts))
	seg_files = []
	for i, p in enumerate(parts):
		heading = (p.get('heading') or '').strip()
		text = (p.get('text') or '').strip()
		if not text:
			continue
		voice_mp3 = os.path.join(tmp, 'v' + str(i) + '.mp3')
		log('[' + slug + '] tts part', i + 1, '/', len(parts))
		tts_long(text, voice_mp3)
		dur = _ffprobe_dur(voice_mp3) + 0.6
		img = images[i % len(images)]
		seg = os.path.join(tmp, 's' + str(i) + '.mp4')
		log('[' + slug + '] render part', i + 1, 'dur', round(dur, 1))
		render_segment(img, heading or text[:80], voice_mp3, seg, dur, i)
		if os.path.exists(seg) and os.path.getsize(seg) > 1000:
			seg_files.append(seg)
	if not seg_files:
		raise RuntimeError('no segments rendered for ' + art)
	joined = os.path.join(tmp, 'joined.mp4')
	log('[' + slug + '] concat', len(seg_files))
	_concat(seg_files, joined)
	final = os.path.join(OUTDIR, 'artdoc' + slug + '' + time.strftime('%Y%m%d%H%M%S') + '.mp4')
	log('[' + slug + '] add music ->', final)
	add_music(joined, final)
	return final, sc
