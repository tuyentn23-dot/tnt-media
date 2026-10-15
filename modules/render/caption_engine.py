# tool: ass+ffmpeg
MODULE = {
	'tool': 'ass+ffmpeg',
	'name': 'render.caption_engine',
	'version': '1.0.0',
	'interface': 'add_captions(in,out) -> path',
	'config_schema': {},
	'deps': ['ffmpeg']
}
# -- coding: utf-8 --
# modules/render/caption_engine.py
# ASS karaoke word-by-word + word-pop
import os, subprocess

UND = chr(95)
Q = chr(39)

def _ff():
	root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
	ff = os.path.join(root, 'tools', 'ffmpeg.exe')
	return ff if os.path.exists(ff) else 'ffmpeg'

def _ts(t, sep=','):
	h = int(t // 3600)
	m = int((t % 3600) // 60)
	s = t % 60
	return str(h).zfill(2) + ':' + str(m).zfill(2) + ':' + (chr(37) + '06.3f') % s

def _ts_ass(t):
	# H:MM:SS.cc
	h = int(t // 3600)
	m = int((t % 3600) // 60)
	s = t % 60
	cs = int((s - int(s)) * 100)
	return str(h) + ':' + str(m).zfill(2) + ':' + str(int(s)).zfill(2) + '.' + str(cs).zfill(2)

# ASS header for Vietnamese captions
ASS_HEADER = '''[Script Info]
ScriptType: v4.00+
PlayResX: 1080
PlayResY: 1920
ScaledBorderAndShadow: yes
WrapStyle: 0

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Default,Arial,72,&H00FFFFFF,&H0000A5FF,&H00000000,&H00000000,-1,0,0,0,100,100,0,0,1,4,2,2,30,30,280,1
Style: Hook,Arial,88,&H0000FFFF,&H000000FF,&H00000000,&H00000000,-1,0,0,0,100,100,0,0,1,5,3,8,30,30,60,1
Style: WordPop,Arial,80,&H00FFFFFF,&H00FF00FF,&H00000000,&H00000000,-1,0,0,0,100,100,0,0,1,5,2,2,30,30,280,1
Style: Karaoke,Arial,72,&H00FFFFFF,&H0000A5FF,&H00000000,&H00000000,-1,0,0,0,100,100,0,0,1,4,2,2,30,30,280,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
'''

def build_ass(segs, out, style_name='WordPop'):
	"""segs: list of (start, end, text).
	Moi seg se duoc chia thanh cac tu, moi tu hien ra theo karaoke timing.
	"""
	lines = [ASS_HEADER]
	for s in segs:
		a, b, txt = s
		# split text into words
		words = txt.split()
		if not words:
			continue
		word_dur = (b - a) / len(words)
		# Option 1: word-by-word lines (each word appears with karaoke)
		parts = []
		for i, w in enumerate(words):
			# karaoke tag: k=centiseconds per word
			cs = int(word_dur * 100)
			parts.append('{' + chr(92) + 'k' + str(cs) + '}' + w)
		line_text = ' '.join(parts)
		lines.append('Dialogue: 0,' + _ts_ass(a) + ',' + _ts_ass(b) + ',' + style_name + ',,0,0,0,,' + line_text)
	open(out, 'w', encoding='utf-8').write(chr(10).join(lines))
	return out

def build_word_pop_ass(segs, out, words_per_group=5):
	"""Word-pop style: nhom 3-4 tu, pop-in + stay + pop-out."""
	lines = [ASS_HEADER]
	for s in segs:
		a, b, txt = s
		words = txt.split()
		if not words:
			continue
		dur = b - a
		n_groups = max(1, (len(words) + words_per_group - 1) // words_per_group)
		group_dur = dur / n_groups
		for gi in range(n_groups):
			grp = words[gi*words_per_group:(gi+1)*words_per_group]
			if not grp:
				continue
			gs = a + gi * group_dur
			ge = gs + group_dur
			gtxt = ' '.join(grp)
			# Pop-in: scale 60->100 in 0.08s
			text = ('{' + chr(92) + 'fscx60' + chr(92) + 'fscy60' + chr(92) + 't(0,80,' + chr(92) + 'fscx100' + chr(92) + 'fscy100)}' + gtxt)
			lines.append('Dialogue: 0,' + _ts_ass(gs) + ',' + _ts_ass(ge) + ',WordPop,,0,0,0,,' + text)
	open(out, 'w', encoding='utf-8').write(chr(10).join(lines))
	return out

def build_karaoke_ass(word_segs, out, max_chars=50, max_gap=0.5):
	"""Karaoke chuan: chia phrase theo CAU, khong noi 2 cau khac nhau tren 1 khung.
	word_segs: list of [start, end, word]. Moi phrase chi chua tu 1 cau.
	"""
	if not word_segs:
		return None
	ws = sorted([(float(s[0]), float(s[1]), str(s[2])) for s in word_segs if len(s) >= 3 and str(s[2]).strip()], key=lambda x: x[0])
	if not ws:
		return None
	# Bat dau phrase moi khi: (a) gap > max_gap, (b) vuot max_chars, (c) tu truoc ket thuc bang dau cau (. ! ?)
	END_PUNCT = ('.', '!', '?', chr(8230))
	phrases = []
	cur = []
	for i in range(len(ws)):
		t0, t1, w = ws[i]
		if not cur:
			cur.append((t0, t1, w))
			continue
		prev_end = cur[-1][1]
		prev_word = cur[-1][2]
		cur_chars = sum(len(x[2]) for x in cur) + len(cur) - 1
		gap = t0 - prev_end
		# Bat dau phrase moi neu gap lon / qua dai / tu truoc ket thuc cau
		prev_ends_sentence = prev_word.endswith(END_PUNCT)
		if gap > max_gap or (cur_chars + 1 + len(w)) > max_chars or prev_ends_sentence:
			phrases.append(cur)
			cur = [(t0, t1, w)]
		else:
			cur.append((t0, t1, w))
	if cur:
		phrases.append(cur)
	# Post-process: neu phrase cuoi < 3 tu VA phrase truoc khong ket cau -> gop lai
	if len(phrases) >= 2:
		last = phrases[-1]
		prev = phrases[-2]
		prev_last_word = prev[-1][2] if prev else ''
		prev_ends_sent = prev_last_word.endswith(END_PUNCT)
		if len(last) < 3 and not prev_ends_sent:
			phrases[-2] = prev + last
			phrases.pop()
	lines = [ASS_HEADER]
	for ph in phrases:
		a = ph[0][0]
		b = ph[-1][1]
		parts = []
		for i in range(len(ph)):
			t0 = ph[i][0]
			t1 = ph[i][1]
			w = ph[i][2]
			if i + 1 < len(ph):
				d = ph[i+1][0] - t0
			else:
				d = t1 - t0
			cs = max(1, int(round(d * 100)))
			parts.append('{' + chr(92) + 'k' + str(cs) + '}' + w)
		text = ' '.join(parts)
		lines.append('Dialogue: 0,' + _ts_ass(a) + ',' + _ts_ass(b) + ',Karaoke,,0,0,0,,' + text)
	open(out, 'w', encoding='utf-8').write(chr(10).join(lines))
	return out

def _wrap(text, max_chars=22):
	words = str(text or '').split()
	if not words:
		return []
	out = []
	cur = ''
	for w in words:
		cand = (cur + ' ' + w).strip()
		if len(cand) <= max_chars:
			cur = cand
		else:
			if cur:
				out.append(cur)
			cur = w
	if cur:
		out.append(cur)
	return out




def _split_hook(text):
	s = str(text or '').strip()
	if not s:
		return ['', '']
	if len(s) <= 34:
		return [s, '']
	import re as _re
	target = int(len(s) * 0.58)
	def _best(pat):
		ms = list(_re.finditer(pat, s))
		if not ms:
			return None
		best = min(ms, key=lambda m: abs(m.end() - target))
		return best.end()
	cut = _best(r'[.!?]')
	if cut is None or cut < 6 or cut > len(s) - 6:
		cut = _best('[,;:]')
	if cut is not None and 6 <= cut <= len(s) - 6:
		p1 = s[:cut].strip()
		p2 = s[cut:].strip()
		if p1 and p2:
			return [p1, p2]
	words = s.split()
	if len(words) < 4:
		return [s, '']
	mid = (len(words) + 1) // 2
	return [' '.join(words[:mid]), ' '.join(words[mid:])]



def build_hook_ass(hook_text, duration, out_path):
	parts = _split_hook(hook_text)
	p1 = _wrap(parts[0], 22)
	p2 = _wrap(parts[1], 22)
	if not p1 and not p2:
		return None
	mid_t = round(duration * 0.45, 3)
	end_t = round(duration, 3)
	fade_ms = 500
	hd = []
	hd.append('[Script Info]')
	hd.append('ScriptType: v4.00+')
	hd.append('PlayResX: 1080')
	hd.append('PlayResY: 1920')
	hd.append('WrapStyle: 0')
	hd.append('')
	hd.append('[V4+ Styles]')
	hd.append('Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding')
	hd.append('Style: HookTop,Arial,70,&H00FFFFFF,&H000000FF,&H00000000,&H88000000,-1,0,0,0,100,100,0,0,3,4,3,8,40,40,150,1')
	hd.append('')
	hd.append('[Events]')
	hd.append('Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text')
	ev = []
	if p1:
		t1 = (chr(92) + 'N').join(p1)
		f1 = '{\fad(' + str(fade_ms) + ',' + str(fade_ms) + ')}'
		ev.append('Dialogue: 0,0:00:00.00,' + _ts_ass(mid_t) + ',HookTop,,0,0,0,,' + f1 + t1)
	if p2:
		t2 = (chr(92) + 'N').join(p2)
		f2 = '{\fad(' + str(fade_ms) + ',' + str(fade_ms + 200) + ')}'
		ev.append('Dialogue: 0,' + _ts_ass(mid_t) + ',' + _ts_ass(end_t) + ',HookTop,,0,0,0,,' + f2 + t2)
	open(out_path, 'w', encoding='utf-8').write(chr(10).join(hd + ev) + chr(10))
	return out_path



def add_captions(video_path, segs, out_path=None, style='wordpop'):
	"""Burn captions vao video.
	style: 'karaoke' (word by word highlight) hoac 'wordpop' (group pop-in)
	"""
	if not out_path:
		out_path = video_path
	# Unique srt/ass name
	d = os.path.dirname(os.path.abspath(video_path))
	base = os.path.splitext(os.path.basename(video_path))[0]
	ass = os.path.join(d, base + '.cap.ass')
	tmp = video_path + '.caps.mp4'
	if style == 'karaoke':
		build_karaoke_ass(segs, ass)
	elif style == 'wordpop':
		build_word_pop_ass(segs, ass)
	else:
		build_ass(segs, ass)
	# Run ffmpeg from d with relative path
	ass_name = base + '.cap.ass'
	# escape for ffmpeg subtitles filter
	ass_esc = ass_name.replace(':', chr(92) + ':')
	vf = 'subtitles=' + ass_esc
	cmd = [_ff(), '-y', '-i', os.path.abspath(video_path), '-vf', vf, '-c:a', 'copy', os.path.abspath(tmp)]
	r = subprocess.run(cmd, capture_output=True, cwd=d)
	if r.returncode == 0 and os.path.exists(tmp):
		os.replace(tmp, os.path.abspath(out_path))
		return True
	return False

if __name__ == '__main__':
	import sys, io
	sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
	# Test
	segs = [
		(0.0, 2.0, 'Xin chào các bạn'),
		(2.0, 4.0, 'Hôm nay chúng ta sẽ khám phá'),
		(4.0, 6.0, 'Điều thú vị bất ngờ'),
	]
	print('Testing word-pop ASS')
	build_word_pop_ass(segs, '_test.ass')
	print('wrote _test.ass', os.path.getsize('_test.ass'))
