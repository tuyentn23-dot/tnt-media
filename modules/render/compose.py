# tool: ffmpeg
# -- coding: utf-8 --
# modules/render/compose.py v1.0.0
# COMPOSE: clip AI tho -> video ngan hap dan
# voiceover + caption karaoke + nhac nen + hook overlay + scale 9:16
import os, sys, json, subprocess, tempfile, shutil, random, glob
U = chr(95)
FKEY = U + U + 'file' + U + U
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(globals()[FKEY]))))
sys.path.insert(0, ROOT)
FFMPEG = os.path.join(ROOT, 'tools', 'ffmpeg.exe')
FONT = os.path.join(ROOT, 'tools', 'font_arial.ttf')
STAR = chr(42)
DOT = chr(46)
MB = 'music' + chr(95) + 'bank'

MODULE = {
	'tool': 'ffmpeg',
	'name': 'render.compose',
	'version': '1.1.0',
	'interface': 'compose(base_video, item, style, out) -> dict',
	'deps': ['render.voice_synth', 'render.caption_engine', 'ffmpeg']
}

W, H, FPS = 1080, 1920, 30


def log(m):
	try:
		print('[compose] ' + str(m), flush=True)
	except Exception:
		pass


def probe_dur(path):
	import re
	try:
		r = subprocess.run([FFMPEG, '-i', path, '-hide_banner'], capture_output=True, text=True, timeout=30, creationflags=0x08000000)
		m = re.search('Duration: (\d+):(\d+):(\d+\.\d+)', r.stderr)
		if m:
			return int(m.group(1)) * 3600 + int(m.group(2)) * 60 + float(m.group(3))
	except Exception:
		pass
	return 0.0


def _run(args, timeout=900):
	return subprocess.run(args, capture_output=True, text=True, timeout=timeout, creationflags=0x08000000)


def build_script_text(item):
	parts = []
	for k in ('hook', 'body', 'payoff', 'cta'):
		v = item.get(k) or ''
		if v:
			parts.append(str(v).strip())
	txt = ' '.join(parts).strip()
	if not txt:
		txt = str(item.get('voiceover_text') or item.get('topic') or item.get('title') or '').strip()
	return txt


def _ffpath(p):
	return str(p).replace(chr(92), '/')


def wrap_text(text, max_chars=22):
	words = str(text or '').split()
	if not words:
		return []
	lines = []
	cur = ''
	for w in words:
		cand = (cur + ' ' + w).strip()
		if len(cand) <= max_chars:
			cur = cand
		else:
			if cur:
				lines.append(cur)
			cur = w
	if cur:
		lines.append(cur)
	return lines

def _esc_drawtext(s):
	t = str(s or '')
	t = t.replace(chr(92), '')
	t = t.replace(':', chr(92) + ':')
	t = t.replace(chr(39), '')
	t = t.replace(chr(37), chr(92) + chr(37))
	return t


def pick_music(topic=''):
	m = glob.glob(os.path.join(ROOT, MB, STAR + DOT + 'wav'))
	if not m:
		m = glob.glob(os.path.join(ROOT, MB, STAR + DOT + 'mp3'))
	return random.choice(sorted(m)) if m else None


def step_scale(base, out, dur=None):
	vf = 'scale=' + str(W) + ':' + str(H) + ':force_original_aspect_ratio=increase,crop=' + str(W) + ':' + str(H) + ',fps=' + str(FPS)
	args = [FFMPEG, '-y', '-i', base, '-vf', vf, '-c:v', 'libx264', '-preset', 'veryfast', '-crf', '20', '-pix_fmt', 'yuv420p', '-an', out]
	r = _run(args)
	return {'ok': os.path.exists(out) and os.path.getsize(out) > 1000, 'path': out, 'err': r.stderr[-300:] if r.stderr else ''}


def step_captions(video, segs, out):
	try:
		from modules.render import caption_engine as ce
		r = ce.add_captions(video, segs, out_path=out, style='karaoke')
		return {'ok': os.path.exists(out) and os.path.getsize(out) > 1000, 'path': out}
	except Exception as e:
		return {'ok': False, 'error': str(e)[:200]}


def _relfont():
	try:
		rel = os.path.relpath(FONT, os.getcwd())
		if not rel.startswith('..'):
			return rel.replace(chr(92), '/')
	except Exception:
		pass
	return FONT.replace(chr(92), '/')


def step_overlay(video, out, hook='', watermark='', brand='#f6ad55'):
	filters = []
	fontrel = _relfont()
	ass_path = None
	if hook:
		try:
			from modules.render import caption_engine as _ce
			d = probe_dur(video)
			if d <= 0:
				d = 12.0
			ass_path = video + '.hook.ass'
			_ce.build_hook_ass(hook, d, ass_path)
		except Exception:
			ass_path = None
	if watermark:
		wm = _esc_drawtext(watermark)
		filters.append('drawtext=fontfile=' + fontrel + ':text=' + chr(39) + wm + chr(39) + ':fontcolor=white@0.85:fontsize=42:x=(w-text_w)/2:y=h-150')
	if not filters and not ass_path:
		shutil.copyfile(video, out)
		return {'ok': True, 'path': out, 'filters': 0}
	vf_parts = []
	if ass_path:
		vf_parts.append('ass=' + os.path.basename(ass_path))
	if filters:
		vf_parts.append(','.join(filters))
	vf = ','.join(vf_parts)
	args = [FFMPEG, '-y', '-i', os.path.abspath(video), '-vf', vf, '-c:v', 'libx264', '-preset', 'veryfast', '-crf', '20', '-pix_fmt', 'yuv420p', '-an', os.path.abspath(out)]
	r = subprocess.run(args, capture_output=True, text=True, timeout=600, creationflags=0x08000000, cwd=os.path.dirname(os.path.abspath(video)))
	if not (os.path.exists(out) and os.path.getsize(out) > 1000):
		shutil.copyfile(video, out)
		return {'ok': True, 'path': out, 'filters': 0, 'note': 'overlay fallback'}
	return {'ok': True, 'path': out, 'filters': len(filters) + (1 if ass_path else 0), 'ass': bool(ass_path)}



def step_mux(video, voice, music, out, music_vol=0.14):
	if not voice or not os.path.exists(voice):
		shutil.copyfile(video, out)
		return {'ok': True, 'path': out, 'mux': 'none'}
	vd = probe_dur(video)
	if vd <= 0:
		vd = 20.0
	voiced = probe_dur(voice)
	pad_v = 0.0
	if voiced > vd + 0.1:
		pad_v = round(voiced - vd + 0.4, 3)
		vd = voiced + 0.4
	vdur = str(round(vd, 3))
	if music and os.path.exists(music):
		fc = "[0:v]tpad=stop_duration=" + str(pad_v) + ":stop_mode=clone[vpad];[1:a]volume=1.0,apad[v];[2:a]volume=" + str(music_vol) + ",aloop=loop=-1:size=2e9[m];[v][m]amix=inputs=2:duration=longest:dropout_transition=2,atrim=0:" + vdur + "[a]"
		args = [FFMPEG, "-y", "-i", video, "-i", voice, "-i", music, "-filter_complex", fc, "-map", "[vpad]", "-map", "[a]", "-c:v", "libx264", "-preset", "veryfast", "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "192k", "-t", vdur, out]
		r = _run(args)
		if os.path.exists(out) and os.path.getsize(out) > 100000:
			return {'ok': True, 'path': out, 'mux': 'voice+music+full'}
		log("mux+music failed: " + str(r.stderr[-200:]))
		try:
			if os.path.exists(out):
				os.remove(out)
		except Exception:
			pass
	fc2 = "[0:v]tpad=stop_duration=" + str(pad_v) + ":stop_mode=clone[vpad];[1:a]volume=1.0,apad,atrim=0:" + vdur + "[a]"
	args2 = [FFMPEG, "-y", "-i", video, "-i", voice, "-filter_complex", fc2, "-map", "[vpad]", "-map", "[a]", "-c:v", "libx264", "-preset", "veryfast", "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "192k", "-t", vdur, out]
	r2 = _run(args2)
	if os.path.exists(out) and os.path.getsize(out) > 100000:
		return {'ok': True, 'path': out, 'mux': 'voice+full'}
	log("mux voice-only failed: " + str(r2.stderr[-200:]))
	try:
		if os.path.exists(out):
			os.remove(out)
	except Exception:
		pass
	shutil.copyfile(video, out)
	return {'ok': True, 'path': out, 'mux': 'fallback-copy'}



def compose(base_video, item, style, out):
	item = item or {}
	style = style or {}
	steps = {}
	tmpbase = os.path.join(ROOT, '_tmp_overlay')
	if not os.path.isdir(tmpbase):
		os.makedirs(tmpbase, exist_ok=True)
	tmp = tempfile.mkdtemp(prefix='compose', dir=tmpbase)
	if not os.path.exists(base_video):
		return {'ok': False, 'error': 'base video missing', 'steps': steps}
	log('base dur=' + str(round(probe_dur(base_video), 2)))
	scaled = os.path.join(tmp, 'scaled.mp4')
	s = step_scale(base_video, scaled)
	steps['scale'] = {'ok': s['ok']}
	if not s['ok']:
		return {'ok': False, 'error': 'scale failed: ' + str(s.get('err')), 'steps': steps}
	# Chuan hoa text: co dau + tach CTA
	try:
		from ops import voice_script as vsc
		scr = vsc.build_script(item)
		sentences = scr.get('sentences') or []
		cta = scr.get('cta') or ''
		text = ' '.join(sentences)
	except Exception:
		sentences = []
		cta = ''
		text = build_script_text(item)
	voice = os.path.join(tmp, 'voice.mp3')
	words = []
	if text or cta:
		try:
			from ops import voice_express as vexp
			base_rate = '-10%'
			vp = style.get('voice_preset')
			if vp == 'excited':
				base_rate = '-5%'
			elif vp == 'calm':
				base_rate = '-15%'
			rv = vexp.synth_express(text, voice, voice=style.get('voice', 'female_north'), base_rate=base_rate, cta=cta, sentences=(sentences or None))
			steps['voice'] = {'ok': rv.get('ok'), 'size': rv.get('size'), 'sentences': rv.get('sentences'), 'has_cta': rv.get('has_cta'), 'mode': 'express'}
			if rv.get('ok'):
				try:
					from modules.render import voice_synth as vs
					full = text + (' ' + cta if cta else '')
					words = vs._proportional_words(full, vs.audio_dur(voice))
				except Exception:
					words = []
		except Exception as e:
			steps['voice'] = {'ok': False, 'error': str(e)[:160]}
	else:
		steps['voice'] = {'ok': False, 'error': 'no script text'}
	cur = scaled
	if words:
		capped = os.path.join(tmp, 'captioned.mp4')
		sc = step_captions(cur, words, capped)
		steps['captions'] = {'ok': sc['ok']}
		if sc['ok']:
			cur = capped
	hook = item.get('hook') or item.get('title') or ''
	wm = style.get('watermark') or ''
	over = os.path.join(tmp, 'overlay.mp4')
	so = step_overlay(cur, over, hook=hook, watermark=wm)
	steps['overlay'] = {'ok': so['ok'], 'filters': so.get('filters')}
	if so['ok']:
		cur = over
	music = pick_music(item.get('topic', '')) if style.get('music', True) else None
	steps['music'] = {'picked': bool(music)}
	sm = step_mux(cur, voice, music, out)
	steps['mux'] = {'ok': sm['ok'], 'mux': sm.get('mux')}
	try:
		shutil.rmtree(tmp, ignore_errors=True)
	except Exception:
		pass
	dur = probe_dur(out) if os.path.exists(out) else 0
	return {'ok': os.path.exists(out) and os.path.getsize(out) > 1000, 'path': out, 'duration': round(dur, 2), 'script': text, 'steps': steps}
