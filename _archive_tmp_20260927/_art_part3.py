

def _ffprobe_dur(path):
	cmd = [FFMPEG, '-hide_banner', '-i', path, '-f', 'null', '-']
	r = subprocess.run(cmd, capture_output=True, text=True, encoding='utf-8', errors='replace')
	import re
	m = re.findall(r'time=(d+):(d+):(d+.d+)', r.stderr)
	if not m:
		return 0.0
	h, mm, ss = m[-1]
	return int(h) * 3600 + int(mm) * 60 + float(ss)


def _font():
	for f in ['C:/Windows/Fonts/arialbd.ttf', 'C:/Windows/Fonts/arial.ttf']:
		if os.path.exists(f):
			return f
	return None


def render_segment(img, text, audio_mp3, out_mp4, dur, idx):
	"""One segment: image with slow Ken Burns zoom + voice audio + caption."""
	fps = 30
	d = max(3.0, float(dur))
	scale_w = 1536
	frames = int(d * fps)
	zoom = "min(zoom+0.0008,1.25)"
	vf = ('scale=' + str(scale_w) + ':-2,'
		+ 'zoompan=z=' + chr(39) + zoom + chr(39) + ':d=' + str(frames) + ':s=1280x720:fps=' + str(fps))
	font = _font()
	if font and text:
		safe = text.replace(':', ' ').replace(chr(39), ' ').replace('%', ' ')
		vf += ',drawtext=fontfile=' + font + ':text=' + chr(39) + safe + chr(39)
		vf += ':fontcolor=white:fontsize=34:box=1:boxcolor=black@0.45:boxborderw=18'
		vf += ':x=(w-text_w)/2:y=h-140'
	cmd = [FFMPEG, '-y', '-hide_banner', '-loop', '1', '-i', img, '-i', audio_mp3,
		'-map', '0:v:0', '-map', '1:a:0',
		'-vf', vf, '-t', str(d),
		'-c:v', 'libx264', '-preset', 'veryfast', '-crf', '23', '-pix_fmt', 'yuv420p',
		'-c:a', 'aac', '-b:a', '160k', '-ar', '44100', '-ac', '2',
		'-shortest', out_mp4]
	subprocess.run(cmd, capture_output=True, text=True, encoding='utf-8', errors='replace')
	return out_mp4


def _concat(parts, out_mp4):
	lst = os.path.join(OUTDIR, '_concat_list.txt')
	open(lst, 'w', encoding='utf-8').write(''.join("file '" + p.replace(chr(92), '/') + "'" + chr(10) for p in parts))
	cmd = [FFMPEG, '-y', '-hide_banner', '-f', 'concat', '-safe', '0', '-i', lst,
		'-c', 'copy', out_mp4]
	subprocess.run(cmd, capture_output=True, text=True, encoding='utf-8', errors='replace')
	return out_mp4
