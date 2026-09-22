import numpy as np, wave, os
OUT='output/music'
os.makedirs(OUT, exist_ok=True)
SR=44100
def tone(f, d, vol=0.3):
	n=int(SR*d)
	t=np.linspace(0, d, n, False)
	x=np.sin(np.multiply(np.multiply(2, np.pi), np.multiply(f, t)))
	x=np.multiply(vol, x)
	env=np.exp(np.multiply(-3, t))
	x=np.multiply(x, env)
	return x
notes=[523,587,659,698,784,880,784,659,587,523,659,784]
beat=0.25
parts=[tone(f,beat) for f in notes]
song=np.concatenate(parts)
song=np.tile(song, 3)
song=np.concatenate([song, tone(523, 1.0, 0.4)])
mx=np.max(np.abs(song))
song=np.multiply(np.divide(song, mx), 0.8)
song=np.multiply(song, 32767).astype(np.int16)
path=os.path.join(OUT, 'cat_upbeat.wav')
w=wave.open(path, 'w')
w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR)
w.writeframes(song.tobytes()); w.close()
print('WROTE', path, len(song)/SR)
