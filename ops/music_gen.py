# music_gen.py - sinh nhac nen procedural (tab)
import os, numpy as np, wave, random
ROOT = os.getcwd()
MD = os.path.join(ROOT, 'music_bank')

def _tone(freq, dur, sr=22050, vol=0.3, wave_type='sine'):
	t = np.linspace(0, dur, int(sr * dur), False)
	if wave_type == 'sine':
		w = np.sin(2 * np.pi * freq * t)
	elif wave_type == 'tri':
		w = 2 * np.abs(2 * (t * freq - np.floor(t * freq + 0.5)))-1
	else:
		w = np.sign(np.sin(2 * np.pi * freq * t))
	env = np.minimum(1, np.minimum(t * 20, (dur - t) * 20))
	return w * env * vol
SCALES = {'major': [0,2,4,5,7,9,11], 'minor': [0,2,3,5,7,8,10], 'penta': [0,3,5,7,10]}

def gen_track(out, seed=0, dur=30, bpm=90, mood='chill'):
	os.makedirs(os.path.dirname(out), exist_ok=True)
	random.seed(seed)
	sr = 22050
	scale = SCALES['penta'] if mood=='chill' else SCALES['minor']
	root = random.choice([220, 246, 261, 293, 329])
	beat = 60.0 / bpm
	n = int(sr * dur)
	buf = np.zeros(n)
	# melody note

	tpos = 0.0
	while tpos < dur:
		step = beat * random.choice([0.5, 1, 1])

		deg = random.choice(scale)
		freq = root * (2 ** (deg / 12.0))

		nt = _tone(freq, min(step, dur-tpos), sr, 0.25, random.choice(['sine', 'tri']))
		i = int(tpos * sr)
		nt = nt[:len(buf)-i]
		buf[i:i+len(nt)] += nt
		tpos += step
	# bass

	tpos = 0.0
	while tpos < dur:
		freq = root/2

		bt = _tone(freq, beat * 2, sr, 0.2, 'sine')
		i = int(tpos * sr)
		bt = bt[:len(buf)-i]
		buf[i:i+len(bt)] += bt
		tpos += beat * 2
	buf = buf / max(1, np.max(np.abs(buf))) * 0.7

	data = (buf * 32767).astype(np.int16)
	w = wave.open(out, 'w')
	w.setnchannels(1); w.setsampwidth(2); w.setframerate(sr)
	w.writeframes(data.tobytes())
	w.close()
	return out

