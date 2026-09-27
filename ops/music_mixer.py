# music_mixer.py - mix background music under voice with sidechain ducking (ffmpeg)
import os, sys, subprocess, random, glob, shutil
CAND = [os.environ.get("TNT_MEDIA_ROOT"), os.getcwd()] + list(sys.path)
ROOT = next((p for p in CAND if p and os.path.isdir(os.path.join(p, "tools"))), os.getcwd())
FFMPEG = os.path.join(ROOT, "tools", "ffmpeg.exe")


def _probe(path):
	import re
	try:
		r = subprocess.run([FFMPEG, "-i", path], capture_output=True, text=True, timeout=30)
	except Exception:
		return 0.0
	m = re.search(r"Duration: (\d+):(\d+):(\d+\.\d+)", r.stderr)
	if not m:
		return 0.0
	return int(m.group(1))*3600 + int(m.group(2))*60 + float(m.group(3))


def bank_dir():
	d = os.path.join(ROOT, "music_bank")
	if os.path.isdir(d):
		return d
	return os.path.join(ROOT, "assets")


def list_music():
	files = []
	d = bank_dir()
	for ext in ("*.wav", "*.mp3", "*.m4a", "*.ogg"):
		files.extend(glob.glob(os.path.join(d, ext)))
	return sorted(files)


def pick_music(topic=''):
	files = list_music()
	if not files:
		return None
	random.seed(str(topic))
	return random.choice(files)


def _copy(src, out):
	os.makedirs(os.path.dirname(os.path.abspath(out)), exist_ok=True)
	shutil.copy(src, out)
	return out


def mix(voice, music, out, duck=True, music_vol=0.16, voice_vol=1.0, loop=True):
	if not voice or not os.path.exists(voice):
		raise FileNotFoundError(voice)
	os.makedirs(os.path.dirname(os.path.abspath(out)), exist_ok=True)
	if not music or not os.path.exists(music):
		return _copy(voice, out)
	loopargs = ["-stream_loop", "-1"] if loop else []
	if duck:
		fc = ("[1:a]volume=" + str(music_vol) + "[m];[m][0:a]sidechaincompress=threshold=0.03:ratio=8:attack=5:release=250[duck];[0:a][duck]amix=inputs=2:duration=first:dropout_transition=0:normalize=0[out]")
	else:
		fc = ("[1:a]volume=" + str(music_vol) + "[m];[0:a][m]amix=inputs=2:duration=first:dropout_transition=0:normalize=0[out]")
	cmd = [FFMPEG, "-y", "-i", voice] + loopargs + ["-i", music, "-filter_complex", fc, "-map", "[out]", "-shortest", "-c:a", "pcm_s16le", out]
	try:
		subprocess.run(cmd, capture_output=True, text=True, timeout=180, check=True)
		return out
	except Exception:
		return copy(voice, out)


def mix_for(video_id, voice, topic='', out=None, **kw):
	music = pick_music(topic or video_id)
	if out is None:
		out = os.path.join(ROOT, "output", "mixed" + str(video_id) + ".wav")
	return mix(voice, music, out, **kw)
