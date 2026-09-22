# ffmpeg_render.py - fast native renderer (multi-scene, hook, caption, music)
import os, sys, re, json, random, hashlib, subprocess
from ops import voice_engine as VE
from ops import voice_synth as VS
from ops import voice_master as VM
FFMPEG = VE.FFMPEG
ROOT = VE.ROOT
FONT = 'tools/font_arial.ttf'
CAP_COLOR = 'white'
HOOK_COLOR = '0xFFEB3B'
BAR_COLOR = '0xe94560'
W, H, FPS = 720, 1280, 30
SQ_BAR = ';'
COLOR_SRC = 'color=c=0x080a19:s=720x1280:d='
def durf(path):
 return VM.duration(path)

def mp4s(x):
 fs = sorted(os.listdir(x)) if os.path.isdir(x) else []
 return [f for f in fs if f.lower().endswith('.mp4') and not f.startswith('music')]

def pickpool(topic, seed):
 lib = os.path.join(ROOT, 'library')
 d = os.path.join(lib, str(topic).strip().lower())
 files = [os.path.join(d, f) for f in mp4s(d)]
 allf = [os.path.join(lib, s, f) for s in (sorted(os.listdir(lib)) if os.path.isdir(lib) else []) for f in mp4s(os.path.join(lib, s))]
 pool = files or allf
 random.seed(seed)
 random.shuffle(pool)
 return pool

def pick_music(topic):
	import random, glob
	bank = os.path.join(ROOT, 'music_bank')
	if os.path.isdir(bank):
		fs = sorted(glob.glob(os.path.join(bank, '*.wav')))
		if fs:
			return random.choice(fs)
	lib = os.path.join(ROOT, 'library')
	cand = [os.path.join(lib, 'music_bed.wav')]
	return next((c for c in cand if os.path.exists(c)), None)

def escp(p):
 return p.replace(chr(92), chr(47))
def split_text(item, n):
 full = (item.get('hook', '') + ' ' + item.get('body', '') + ' ' + item.get('payoff', '')).strip()
 parts = [p.strip() for p in re.split('[.!?;]+', full) if p.strip()] or [full]
 idx = [min(int(round(i * len(parts) / n)), len(parts) - 1) for i in range(n)]
 return [parts[idx[i]: (idx[i + 1] if i + 1 < n else len(parts))] for i in range(n)]

def split_chunks(item, dur, per=4, min_dur=0.85):
	full = (item.get('hook', '') + ' ' + item.get('body', '') + ' ' + item.get('payoff', '')).strip()
	words = full.split()
	n = max(1, int(round(dur / min_dur)))
	size = max(2, (len(words) + n - 1) // n)
	chunks = [' '.join(words[i:i + size]) for i in range(0, len(words), size)]
	lens = [max(1, len(c)) for c in chunks]
	tot = sum(lens)
	t = 0.0
	out = []
	for c, ln in zip(chunks, lens):
		seg = dur * ln / tot
		out.append((c, round(t, 3), round(t + seg, 3)))
		t += seg
	return out

def write_chunk_files(chunks, tmp):
 n = len(chunks)
 data = [(os.path.join(tmp, 'c' + str(i) + '.txt'), chunks[i][1], chunks[i][2]) for i in range(n)]
 _ = [open(data[i][0], 'w', encoding='utf-8').write(chunks[i][0]) for i in range(n)]
 return data
def ffpath(p):
 return p.replace(chr(92), chr(47))

def one_dt(fp, a, b, font):
 tf = ffpath(fp)
 ff = ffpath(font)
 qt = chr(39)
 en = 'between(t,' + str(a) + ',' + str(b) + ')'
 s = 'drawtext=fontfile=' + ff
 s += ':textfile=' + tf
 s += ':enable=' + qt + en + qt
 s += ':fontsize=52:fontcolor=' + CAP_COLOR + ':borderw=4:bordercolor=black:line_spacing=8'
 s += ':x=(w-text_w)/2:y=0.66 * h'
 return s

def all_dts(caps, tmp):
 return [one_dt(fp, a, b, FONT) for (fp, a, b) in caps]

def _wrap_text(text, width=16):
	import textwrap
	return chr(10).join(textwrap.wrap(text, width=width)[:4])

def hook_drawtext(text, tmp, fs=56):
	fp = os.path.join(tmp, 'hook.txt')
	open(fp, 'w', encoding='utf-8').write(_wrap_text(text, 16))
	ff = ffpath(FONT)
	tf = ffpath(fp)
	qt = chr(39)
	en = 'between(t,0,2.6)'
	s = 'drawtext=fontfile=' + ff + ':textfile=' + tf
	s += ':enable=' + qt + en + qt
	s += ':fontsize=' + str(fs) + ':fontcolor=' + HOOK_COLOR + ':borderw=5:bordercolor=black:line_spacing=12'
	s += ':x=(w-text_w)/2:y=0.22 * h'
	return s

def drawbar(dur):
 return 'drawbox=x=0:y=ih-8:w=iw*t/' + str(dur) + ':h=8:color=' + BAR_COLOR + '@1:t=fill'
def seg_chain(i, frames_per):
	# GIU video motion: chi scale/crop, KHONG zoompan (zoompan lam mat chuyen dong)
	s = '[' + str(i) + ':v]scale=720:1280:force_original_aspect_ratio=increase,crop=720:1280,setsar=1'
	s += ',eq=contrast=1.1:saturation=1.15,vignette=PI/5'
	s += ',trim=duration=' + str(frames_per / 30.0)
	s += ',setpts=PTS-STARTPTS[v' + str(i) + ']'
	return s

def build_filter_multi(sources, caps, frames_per, dur, tmp, hook=None, cta=None):
 n = len(sources)
 chains = ';'.join([seg_chain(i, frames_per) for i in range(n)])
 cin = ''.join(['[v' + str(i) + ']' for i in range(n)])
 merged = chains + ';' + cin + 'concat=n=' + str(n) + ':v=1:a=0[vc]'
 tail = all_dts(caps, tmp) + ([hook_drawtext(hook, tmp)] if hook else []) + [drawbar(dur)]
 return merged + ';[vc]' + ','.join(tail) + ',fade=t=in:st=0:d=0.5:color=white,fade=t=out:st=' + str(max(0.1, dur - 1.2)) + ':d=0.5:color=white[v]'
def _fresh_or_pool(item, seed):
 topic = item.get('topic', '')
 q = item.get('search_query') or topic
 from ops import footage_fetcher as ff
 fresh = ff.fetch_for_topic(topic, query=q, count=10)
 pool = [os.path.relpath(x, ROOT) for x in fresh]
 return pool or pickpool(topic, seed)

def render_gacha(item, out, voice='female_north', preset='cute', seed=None):
	import os as _o, subprocess as sp
	from ops import gacha_sprite as G
	from ops import gacha_anime_render as GAR
	cid = str(item.get('id', 'x'))
	seed = seed if seed is not None else int(hashlib.md5(cid.encode()).hexdigest()[:6], 16)
	os.chdir(ROOT)
	vo = 'output/vo' + chr(95) + cid + '.mp3'
	parts = [item.get('hook', ''), item.get('body', ''), item.get('payoff', '')]
	parts = [p for p in parts if p.strip()]
	VS.synth_parts(parts, vo, voice=voice, preset=preset, gap=0.5)
	dur = min(VM.duration(vo), 58.0)
	g = 'output/gacha' + cid + '.mp4'
	GAR.make_anime(g, dur, seed=seed, pal_idx=(seed % 3), fps=6)
	tmp = '_work'; os.makedirs(tmp, exist_ok=True)
	caps = write_chunk_files(split_chunks(item, dur), tmp)
	hook = item.get('hook', '')
	tail = all_dts(caps, tmp) + ([hook_drawtext(hook, tmp)] if hook else []) + [drawbar(dur)]
	vf = ','.join(tail)
	fc = '[0:v]' + vf + '[v];[1:a]loudnorm=I=-14:TP=-1.5:LRA=11[a]'
	cmd = [FFMPEG, '-y', '-i', g, '-i', vo, '-t', str(dur), '-filter_complex', fc, '-map', '[v]', '-map', '[a]', '-c:v', 'libx264', '-preset', 'veryfast', '-crf', '21', '-pix_fmt', 'yuv420p', '-c:a', 'aac', '-shortest', out]
	r = subprocess.run(cmd, capture_output=True, text=True)
	return out if r.returncode == 0 else (out, r.stderr[-500:])
def render(item, out, voice='female_north', preset='hype', seed=None, music=None, scenes=8):
 cid = str(item.get('id', 'x'))
 seed = seed if seed is not None else int(hashlib.md5(cid.encode()).hexdigest()[:6], 16)
 os.makedirs(os.path.join(ROOT, 'output'), exist_ok=True)
 os.chdir(ROOT)
 vo = 'output/vo_' + cid + '.mp3'
 full = (item.get('hook', '') + ' ' + item.get('body', '') + ' ' + item.get('payoff', '')).strip()
 parts = [item.get('hook', ''), item.get('body', ''), item.get('payoff', '')]
 parts = [p for p in parts if p.strip()]
 VS.synth_parts(parts, vo, voice=voice, preset=preset, gap=0.5)
 dur = min(VM.duration(vo), 58.0)
 chunks = split_chunks(item, dur)
 pool = _fresh_or_pool(item, seed)
 music = music or pick_music(item.get('topic', ''))
 n = max(2, min(scenes, len(pool))) if pool else 0
 srcs = [os.path.relpath(pp, ROOT) for pp in pool[:n]]
 tmp = '_work'; os.makedirs(tmp, exist_ok=True)
 caps = write_chunk_files(chunks, tmp)
 fper = max(1, int((dur / max(1, n)) * FPS))
 hook = item.get('hook', '')
 cta = item.get('question', '') or ''
 vf = build_filter_multi(srcs, caps, fper, dur, tmp, hook=hook, cta=cta) if srcs else 'scale=720:1280[vc];[vc]'+','.join(all_dts(caps, tmp) + [hook_drawtext(hook, tmp), drawbar(dur)])
 vin = []
 _ = [vin.extend(['-stream_loop', '-1', '-i', s]) for s in srcs]
 vin = vin or ['-f', 'lavfi', '-i', COLOR_SRC + str(dur)]
 music_in = ['-stream_loop', '-1', '-i', music] if music else []
 aidx = len(srcs); p1 = vf + ';[' + str(aidx) + ':a]loudnorm=I=-14:TP=-1.5:LRA=11[vo]'
 bidx = aidx + 1; p2 = (';[' + str(bidx) + ':a]volume=-14dB[bg];[bg][vo]amix=inputs=2:duration=first:weights=1 0.4[a]' if music else ';[vo]anull[a]')
 fc = p1 + p2
 enc = ['-t', str(dur), '-filter_complex', fc, '-map', '[v]', '-map', '[a]', '-c:v', 'libx264', '-preset', 'veryfast', '-crf', '21', '-pix_fmt', 'yuv420p', '-c:a', 'aac', '-b:a', '192k', '-shortest', out]
 cmd = [FFMPEG, '-y'] + vin + ['-i', vo] + music_in + enc
 r = subprocess.run(cmd, capture_output=True, text=True)
 return out if r.returncode == 0 else (out, r.stderr[-600:])
def set_style(cap=None, hook=None, bar=None):
	global CAP_COLOR, HOOK_COLOR, BAR_COLOR
	CAP_COLOR = cap or CAP_COLOR
	HOOK_COLOR = hook or HOOK_COLOR
	BAR_COLOR = bar or BAR_COLOR
	return (CAP_COLOR, HOOK_COLOR, BAR_COLOR)

def cta_drawtext(text, tmp, fs=48, dur_c=7):
	fp = os.path.join(tmp, 'cta.txt')
	open(fp, 'w', encoding='utf-8').write(_wrap_text(text, 20))
	ff = ffpath(FONT)
	tf = ffpath(fp)
	qt = chr(39)
	en = qt + 'between(t,' + str(dur_c) + ',' + str(dur_c + 4) + ')' + qt
	s = 'drawtext=fontfile=' + ff + ':textfile=' + tf
	s += ':enable=' + en
	s += ':fontsize=' + str(fs) + ':fontcolor=0x00E5FF:borderw=5:bordercolor=black:line_spacing=10'
	s += ':x=(w-text_w)/2:y=0.40 * h'
	return s


def teaser_drawtext(tmp, fs=46):
	fp = os.path.join(tmp, 'teaser.txt')
	open(fp, 'w', encoding='utf-8').write('Nhung con nua...')
	ff = ffpath(FONT)
	tf = ffpath(fp)
	qt = chr(39)
	en = qt + 'between(t,3.5,5.5)' + qt
	s = 'drawtext=fontfile=' + ff + ':textfile=' + tf
	s += ':enable=' + en
	s += ':fontsize=' + str(fs) + ':fontcolor=0xFFEB3B:borderw=4:bordercolor=black'
	s += ':x=(w-text_w)/2:y=0.15 * h'
	return s


