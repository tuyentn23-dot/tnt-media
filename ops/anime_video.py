# anime_video.py - AI anime image -> MV with edge-tts voice + ducked music
import os, sys, subprocess, hashlib
CAND = [os.environ.get("TNT_MEDIA_ROOT"), os.getcwd()] + list(sys.path)
ROOT = next((p for p in CAND if p and os.path.isdir(os.path.join(p, "tools"))), os.getcwd())
sys.path.insert(0, ROOT)
FFMPEG = os.path.join(ROOT, "tools", "ffmpeg.exe")
AIDIR = os.path.join(ROOT, "output", "ai_anime")


def _safe(s):
	return hashlib.md5(s.encode("utf-8")).hexdigest()[:12]


def gen_images(prompt, n=6, style='anime style, cinematic, high detail, 4k', outdir=None, timeout=60):
	import requests, urllib.parse
	outdir = outdir or AIDIR
	os.makedirs(outdir, exist_ok=True)
	paths = []
	for i in range(n):
		p = prompt + ', ' + style
		seed = int(hashlib.md5((p + str(i)).encode("utf-8")).hexdigest()[:6], 16) % 1000000
		url = 'https://image.pollinations.ai/prompt/' + urllib.parse.quote(p) + '?width=768&height=1024&nologo=true&model=flux&seed=' + str(seed) + '&enhance=true'
		dst = os.path.join(outdir, _safe(p + str(i)) + '.jpg')
		if os.path.exists(dst) and os.path.getsize(dst) > 5000:
			paths.append(dst)
			continue
		for attempt in range(3):
			try:
				r = requests.get(url, timeout=timeout)
				if r.status_code == 200 and len(r.content) > 5000:
					open(dst, 'wb').write(r.content)
					paths.append(dst)
					break
			except Exception:
				pass
	return paths

def mux(video, audio, out):
	cmd = [FFMPEG, '-y', '-i', video, '-i', audio, '-c:v', 'copy', '-c:a', 'aac', '-b:a', '160k', '-shortest', out]
	subprocess.run(cmd, capture_output=True, timeout=180)
	return out


def build_anime_video(item, out, n_images=6, dur=12.0, fps=8, voice='female_north', preset='hype', topic=None):
	from ops import anime_ai_render as aa
	from ops import voice_synth
	from ops import music_mixer
	cid = str(item.get('id', 'a'))
	prompt = item.get('prompt') or (item.get('hook', '') + ', ' + item.get('body', ''))
	imgs = gen_images(prompt, n=n_images)
	if len(imgs) < 1:
		return None
	silent = os.path.join(ROOT, 'output', 'anmv' + cid + '.mp4')
	aa.make_mv(imgs, silent, dur=dur, fps=fps)
	text = item.get('hook', '') + '. ' + item.get('body', '') + '. ' + item.get('payoff', '')
	vo = os.path.join(ROOT, 'output', 'vo_anmv' + cid + '.mp3')
	voice_synth.synth(text, vo, voice=voice, preset=preset, maxlen=4000)
	mixed = os.path.join(ROOT, 'output', 'mix_anmv_' + cid + '.wav')
	music_mixer.mix_for(cid, vo, topic=topic or item.get('topic', ''), out=mixed, duck=True)
	return mux(silent, mixed, out)
