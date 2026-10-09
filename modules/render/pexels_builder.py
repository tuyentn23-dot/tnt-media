MODULE = {
	'name': 'render.pexels_builder',
	'version': '1.0.0',
	'interface': 'build(query,out) -> dict',
	'config_schema': {},
	'deps': ['ops.pexels']
}
# -- coding: utf-8 --
# modules/render/pexels_builder.py
# Build video tu Pexels footage moi (theo topic)
import os, sys, subprocess, random, json
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from modules.render import pexels_fetch as pf
from modules.render import beat_engine as be

BS = chr(92)

def _ff():
	root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
	ff = os.path.join(root, 'tools', 'ffmpeg.exe')
	return ff if os.path.exists(ff) else 'ffmpeg'

def _dur(path):
	import re
	r = subprocess.run([_ff(), '-i', path, '-hide_banner'], capture_output=True, text=True)
	m = re.search('Duration: ([0-9]+):([0-9]+):([0-9.]+)', r.stderr)
	if not m:
		return 0.0
	return int(m.group(1)) * 3600 + int(m.group(2)) * 60 + float(m.group(3))

def _cut(src, out, start, dur, zoom='kenburns'):
	if zoom == 'punch':
		z = 'min(1.3' + BS + ',1+on/9)'
	elif zoom == 'pulse':
		z = '1.05+0.08' + chr(42) + 'sin(on/8)'
	else:
		z = '1+on/2000'
	vf = ('scale=1080:1920:force_original_aspect_ratio=increase,'
	 'crop=1080:1920,setsar=1,'
	 'zoompan=z=' + z + ':d=1:s=1080x1920:fps=30')
	cmd = [_ff(), '-y', '-ss', str(start), '-i', src, '-t', str(dur),
		'-vf', vf, '-an', '-c:v', 'libx264', '-preset', 'veryfast',
		'-pix_fmt', 'yuv420p', out]
	r = subprocess.run(cmd, capture_output=True)
	return r.returncode == 0 and os.path.exists(out) and os.path.getsize(out) > 1000

TRANS = ['fade', 'slideleft', 'slideright', 'wipeleft', 'wiperight',
	'circleopen', 'circleclose', 'smoothleft', 'smoothright', 'dissolve']

def _join(segs, out, xd=0.5):
	if len(segs) == 1:
		import shutil
		shutil.copy(segs[0], out)
		return True
	inputs = []
	for s in segs:
		inputs += ['-i', s]
	filt = []
	prev = '0:v'
	off = 0.0
	for i in range(1, len(segs)):
		sd = _dur(segs[i-1])
		off += (sd - xd)
		lbl = 'v' + str(i)
		t = random.choice(TRANS)
		filt.append('[' + prev + '][' + str(i) + ':v]xfade=transition=' + t + ':duration=' + str(xd) + ':offset=' + str(off) + '[' + lbl + ']')
		prev = lbl
	fc = ';'.join(filt)
	cmd = [_ff(), '-y'] + inputs + ['-filter_complex', fc,
		'-map', '[' + prev + ']', '-c:v', 'libx264', '-preset', 'veryfast',
		'-pix_fmt', 'yuv420p', out]
	r = subprocess.run(cmd, capture_output=True)
	return r.returncode == 0 and os.path.exists(out)

def _fade_out(path):
	d = _dur(path)
	if d < 1:
		return False
	fs = max(0, d - 0.4)
	tmp = path + '.fade.mp4'
	vf = 'fade=t=out:st=' + str(round(fs, 2)) + ':d=0.4'
	af = 'afade=t=out:st=' + str(round(fs, 2)) + ':d=0.4'
	cmd = [_ff(), '-y', '-i', path, '-vf', vf, '-af', af,
		'-c:v', 'libx264', '-preset', 'veryfast', '-pix_fmt', 'yuv420p',
		'-c:a', 'aac', tmp]
	r = subprocess.run(cmd, capture_output=True, timeout=120)
	if r.returncode == 0 and os.path.exists(tmp):
		os.replace(tmp, path)
		return True
	return False

def build(query, out, music=None, seg_dur=2.0, n_segs=5, voice_text=None, captions=None):
	import shutil
	print('[1] Fetch Pexels: ' + query, flush=True)
	clips = pf.fetch_for_topic(query, n=n_segs + 2)
	if len(clips) < 2:
		try:
			from modules.render import stock_fallback as sfb
			fb = sfb.fallback_for_topic(query, n=n_segs + 2, need=2)
			if fb:
				clips = list(clips) + list(fb)
				print('[1b] fallback clips: ' + str(len(fb)), flush=True)
		except Exception as _fbe:
			print('[1b] fallback err: ' + str(_fbe)[:120], flush=True)
	if len(clips) < 2:
		return {'ok': False, 'err': 'no pexels clips'}
	print('[2] Got ' + str(len(clips)) + ' clips', flush=True)
	tmp = os.path.join(os.path.dirname(out) or '.', '_pb_tmp')
	shutil.rmtree(tmp, ignore_errors=True)
	os.makedirs(tmp, exist_ok=True)
	segs = []
	zs = ['kenburns', 'punch', 'pulse']
	for i, c in enumerate(clips[:n_segs]):
		sp = os.path.join(tmp, 'seg' + str(i) + '.mp4')
		sd = _dur(c)
		off = 0.0
		if sd > seg_dur + 1:
			off = random.uniform(0, sd - seg_dur - 0.5)
		if _cut(c, sp, off, seg_dur, zs[i % 3]):
			segs.append(sp)
	print('[3] Cut ' + str(len(segs)) + ' segs', flush=True)
	if len(segs) < 2:
		return {'ok': False, 'err': 'few segs'}
	joined = os.path.join(tmp, 'joined.mp4')
	if not _join(segs, joined, 0.5):
		return {'ok': False, 'err': 'join fail'}
	shutil.copy(joined, out)
	print('[4] Joined: ' + str(round(_dur(out), 2)) + 's', flush=True)
	
	cap_timings = None
	if voice_text:
		from modules.render import voice_sync as vsync
		sents = vsync.split_sentences(voice_text)
		vo_path = out + '.vo.mp3'
		va, cap_timings = vsync.synth_sentences(sents, vo_path)
		if va:
			from ops import vids_post as vp
			vp.mux_audio(out, va)
	if cap_timings is None:
		cap_timings = []
	print('[5] Voice OK', flush=True)
	
	if not music:
		music = 'assets/music_clips/clip_0_0.mp3'
	if os.path.exists(music):
		tmp2 = out + '.mus.mp4'
		d = _dur(out)
		fc = '[1:a]volume=0.10[bg];[0:a][bg]amix=inputs=2:duration=first[aout]'
		cmd = [_ff(), '-y', '-i', out, '-stream_loop', '-1', '-i', music, '-filter_complex', fc,
			'-map', '0:v', '-map', '[aout]', '-c:v', 'copy', '-c:a', 'aac', '-t', str(d), tmp2]
		r = subprocess.run(cmd, capture_output=True, timeout=120)
		if r.returncode == 0 and os.path.exists(tmp2):
			shutil.move(tmp2, out)
		print('[6] Music OK', flush=True)
	
	if captions:
		from modules.render import caption_engine as ce
		d = _dur(out)
		if cap_timings:
			segs_cap = []
			for i in range(min(len(captions), len(cap_timings))):
				start, end, _ = cap_timings[i];
				segs_cap.append((start, end, captions[i]))
		else:
			n = len(captions) + 1
			step = d / n
			segs_cap = []
			t = 0.0
			for c in captions:
				segs_cap.append((t, t + step, c))
				t += step
		ce.add_captions(out, segs_cap, out, style='wordpop')
		print('[7] Captions OK', flush=True)
	
	_fade_out(out)
	print('[8] Fade OK', flush=True)
	return {'ok': True, 'path': out, 'dur': _dur(out)}

def build_from_content(content_key):
	data = json.load(open('content_vi.json', encoding='utf-8'))
	if content_key not in data:
		return {'ok': False, 'err': 'key not found'}
	c = data[content_key]
	return build(
		query=(c.get('query') or c.get('folder') or 'generic'),
		out=c['out'], music='assets/music_clips/clip_0_0.mp3',
		seg_dur=3.0, n_segs=8,
		voice_text=c['voice'], captions=c['captions']
	)
