

def add_music(video_mp4, out_mp4):
	if not os.path.exists(MUSIC):
		return video_mp4
	dur = ffprobe_dur(video_mp4)
	if dur <= 0:
		return video_mp4
	cmd = [FFMPEG, '-y', '-hide_banner', '-i', video_mp4, '-stream_loop', '-1', '-i', MUSIC,
		'-filter_complex', '[1:a]volume=0.15,afade=t=in:st=0:d=2[m];[0:a][m]amix=inputs=2:duration=first:dropout_transition=0[a]',
		'-map', '0:v:0', '-map', '[a]', '-c:v', 'copy', '-c:a', 'aac', '-b:a', '160k', '-shortest', out_mp4]
	subprocess.run(cmd, capture_output=True, text=True, encoding='utf-8', errors='replace')
	return out_mp4 if os.path.exists(out_mp4) else video_mp4


def build_art_video(art, facts, images, slug, sections=8, voice_only=False):
	"""Full pipeline: script -> per-part voice -> segments -> concat -> music."""
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
	n = len(parts)
	for i, p in enumerate(parts):
		heading = (p.get('heading') or '').strip()
		text = (p.get('text') or '').strip()
		if not text:
			continue
		voice_mp3 = os.path.join(tmp, 'v' + str(i) + '.mp3')
		log('[' + slug + '] tts part', i + 1, '/', n)
		tts_long(text, voice_mp3)
		dur = ffprobe_dur(voice_mp3) + 0.6
		img = images[i % len(images)]
		seg = os.path.join(tmp, 's' + str(i) + '.mp4')
		cap = heading or (text[:80])
		log('[' + slug + '] render part', i + 1, 'dur', round(dur, 1))
		render_segment(img, cap, voice_mp3, seg, dur, i)
		if os.path.exists(seg) and os.path.getsize(seg) > 1000:
			seg_files.append(seg)
	if not seg_files:
		raise RuntimeError('no segments rendered for ' + art)
	joined = os.path.join(tmp, 'joined.mp4')
	log('[' + slug + '] concat', len(seg_files), 'segments')
	_concat(seg_files, joined)
	final = os.path.join(OUTDIR, 'artdoc' + slug + '' + time.strftime('%Y%m%d%H%M%S') + '.mp4')
	log('[' + slug + '] add music ->', final)
	_add_music(joined, final)
	return final, sc
