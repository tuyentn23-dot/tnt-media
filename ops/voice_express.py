# ops/voice_express.py - TTS co ngu dieu: chia cau, pause, rate/pitch theo loai cau
import os, sys, re, subprocess, tempfile
U = chr(95)
FKEY = U + U + 'file' + U + U
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(globals()[FKEY])))
sys.path.insert(0, ROOT)
FFMPEG = os.path.join(ROOT, 'tools', 'ffmpeg.exe')


def log(m):
	try:
		print('[voice_express] ' + str(m), flush=True)
	except Exception:
		pass


def _is_question(s):
	return s.strip().endswith('?') or s.strip().endswith(chr(65311))


def _is_exclaim(s):
	return s.strip().endswith('!') or s.strip().endswith(chr(65281))


def _split_sentences(text):
	if not text:
		return []
	# Chia theo . ! ? (ca ASCII va fullwidth)
	punct = chr(46) + chr(33) + chr(63) + chr(65311) + chr(65281)
	parts = []
	cur = ''
	for ch in str(text).strip():
		cur += ch
		if ch in punct:
			parts.append(cur.strip())
			cur = ''
	if cur.strip():
		parts.append(cur.strip())
	out = []
	for p in parts:
		p = p.strip()
		if not p:
			continue
		# Chi merge neu cau ngan VA khong co dau ket cau (fragment that su)
		ends_punct = p and p[-1] in punct
		if (not ends_punct) and len(p) < 12 and out:
			out[-1] = out[-1] + ' ' + p
		else:
			out.append(p)
	return out

def _synth_one(text, out_mp3, voice='female_north', rate='-10%', pitch='+0Hz'):
	from modules.render import voice_synth as vsp
	r = vsp.synth_words(text, out_mp3, voice=voice, rate=rate, pitch=pitch, preset='default', attempts=2)
	return r



def _concat_with_pause(audio_files, pauses, out_mp3):
	if not audio_files:
		return False
	import shutil
	if len(audio_files) == 1:
		shutil.copyfile(audio_files[0], out_mp3)
		return True
	tmpd = tempfile.mkdtemp(prefix='vexp')
	inputs = []
	filter_parts = []
	idx = 0
	for i, af in enumerate(audio_files):
		inputs.extend(['-i', af])
		filter_parts.append('[' + str(idx) + ':a]aresample=24000,aformat=sample_fmts=fltp:channel_layouts=mono[a' + str(idx) + ']')
		idx += 1
		if i < len(pauses):
			pv = pauses[i]
			if pv > 0.05:
				sil = os.path.join(tmpd, 's' + str(i) + '.mp3')
				subprocess.run([FFMPEG, '-y', '-f', 'lavfi', '-i', 'anullsrc=r=24000:cl=mono', '-t', str(pv), '-c:a', 'libmp3lame', '-b:a', '128k', sil], capture_output=True, creationflags=0x08000000)
				inputs.extend(['-i', sil])
				filter_parts.append('[' + str(idx) + ':a]aresample=24000,aformat=sample_fmts=fltp:channel_layouts=mono[a' + str(idx) + ']')
				idx += 1
	concat_in = ''.join('[a' + str(i) + ']' for i in range(idx))
	fc = ';'.join(filter_parts) + ';' + concat_in + 'concat=n=' + str(idx) + ':v=0:a=1[out]'
	cmd = [FFMPEG, '-y'] + inputs + ['-filter_complex', fc, '-map', '[out]', '-c:a', 'libmp3lame', '-b:a', '128k', '-ar', '24000', out_mp3]
	r = subprocess.run(cmd, capture_output=True, text=True, creationflags=0x08000000)
	if r.returncode != 0:
		log('concat err: ' + str(r.stderr[-300:]))
	try:
		shutil.rmtree(tmpd, ignore_errors=True)
	except Exception:
		pass
	return os.path.exists(out_mp3) and os.path.getsize(out_mp3) > 0


def synth_express(text, out_mp3, voice='female_north', base_rate='-10%', cta=None, cta_pause=0.8):
	# Chia cau, TTS tung cau, ghep lai voi pause
	sentences = _split_sentences(text)
	if not sentences:
		return {'ok': False, 'error': 'empty text'}
	if cta:
		cta = cta.strip()
	tmpd = tempfile.mkdtemp(prefix='vexp2')
	audio_files = []
	pauses = []
	log('sentences=' + str(len(sentences)) + ' cta=' + str(bool(cta)))
	for i, s in enumerate(sentences):
		# Chon rate/pitch theo loai cau
		if _is_question(s):
			pr = '+0%'
			pp = '+15Hz'
		elif _is_exclaim(s):
			pr = '+5%'
			pp = '+25Hz'
		else:
			pr = base_rate
			pp = '+0Hz'
		ap = os.path.join(tmpd, 's' + str(i) + '.mp3')
		r = _synth_one(s, ap, voice=voice, rate=pr, pitch=pp)
		if r.get('ok') and os.path.exists(ap) and os.path.getsize(ap) > 0:
			audio_files.append(ap)
			# Pause sau cau
			if i < len(sentences) - 1:
				pauses.append(0.4)
			else:
				pauses.append(0.5 if not cta else cta_pause)
		else:
			log('synth fail sentence ' + str(i) + ': ' + str(r.get('error'))[:80])
	if not audio_files:
		return {'ok': False, 'error': 'all sentences failed'}
	# Them CTA rieng
	if cta:
		ap = os.path.join(tmpd, 'cta.mp3')
		r = _synth_one(cta, ap, voice=voice, rate='-5%', pitch='+10Hz')
		if r.get('ok') and os.path.exists(ap) and os.path.getsize(ap) > 0:
			audio_files.append(ap)
			pauses.append(0.0)
	# Ghep
	ok = _concat_with_pause(audio_files, pauses, out_mp3)
	try:
		import shutil
		shutil.rmtree(tmpd, ignore_errors=True)
	except Exception:
		pass
	if not ok:
		return {'ok': False, 'error': 'concat failed'}
	return {'ok': True, 'path': out_mp3, 'size': os.path.getsize(out_mp3), 'sentences': len(sentences), 'has_cta': bool(cta), 'voice': voice}
