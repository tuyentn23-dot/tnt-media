# beat_sync.py - onset/beat detection via ffmpeg PCM + numpy energy flux
import os, sys, subprocess, wave
import numpy as np
CAND = [os.environ.get("TNT_MEDIA_ROOT"), os.getcwd()] + list(sys.path)
ROOT = next((p for p in CAND if p and os.path.isdir(os.path.join(p, "tools"))), os.getcwd())
FFMPEG = os.path.join(ROOT, "tools", "ffmpeg.exe")

def _decode(path, sr=22050, dur=None):
	cmd = [FFMPEG, "-v", "error", "-i", path]
	if dur:
		cmd += ["-t", str(dur)]
	cmd += ["-ac", "1", "-ar", str(sr), "-f", "s16le", "-"]
	r = subprocess.run(cmd, capture_output=True)
	a = np.frombuffer(r.stdout, dtype=np.int16).astype(np.float32) / 32768.0
	return a, sr

def detect_beats(audio, sr=22050, hop=512, dur=None, sensitivity=1.3):
	y, sr = _decode(audio, sr=sr, dur=dur)
	if y.size == 0:
		return []
	n = len(y) // hop
	frames = y[:n*hop].reshape(n, hop)
	energy = np.sqrt((frames**2).mean(axis=1) + 1e-9)
	flux = np.diff(energy, prepend=energy[0])
	flux[flux < 0] = 0.0
	if flux.max() > 0:
		flux = flux / flux.max()
	thr = flux.mean() + sensitivity*flux.std()
	peaks = []
	last = -10
	tmin = 0.18
	for i in np.where(flux > thr)[0]:
		t = i*hop / float(sr)
		if t - last >= tmin:
			peaks.append(t)
			last = t
	return peaks

def beat_sync(clips, beats, duration):
	if not clips:
		return []
	beats = [b for b in beats if 0 < b < duration]
	if len(beats) < 2:
		n = len(clips)
		seg = duration / float(n)
		return [(c, i*seg, seg) for i, c in enumerate(clips)]
	cuts = [0.0] + beats + [duration]
	plan = []
	ci = 0
	for i in range(len(cuts) - 1):
		s = cuts[i]
		e = cuts[i + 1]
		if e - s < 0.12:
			continue
		plan.append((clips[ci % len(clips)], s, e - s))
		ci += 1
	return plan

def snap_clips(clips, audio, duration, sr=22050):
	beats = detect_beats(audio, sr=sr, dur=duration)
	return beat_sync(clips, beats, duration)
