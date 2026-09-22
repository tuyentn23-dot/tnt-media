import numpy as np, wave, os
OUT='output/music'
os.makedirs(OUT, exist_ok=True)
SR=44100
def meow(f0, dur, vol=0.5):
	n=int(np.multiply(SR, dur))
	t=np.linspace(0, dur, n, False)
	freq=np.multiply(f0, np.add(1.0, np.multiply(0.15, np.sin(np.multiply(np.multiply(2, np.pi), np.multiply(4.0, t))))))
	ph=np.multiply(np.multiply(2, np.pi), np.cumsum(freq))/SR
	x=np.sin(ph)
	x=np.add(x, np.multiply(0.3, np.sin(np.multiply(2.0, ph))))
	env=np.multiply(np.exp(np.multiply(-3.0, t)), np.minimum(1.0, np.multiply(20.0, t)))
	return np.multiply(np.multiply(vol, x), env)
p1=meow(620, 0.5)
p2=meow(700, 0.4)
p3=meow(560, 0.6)
gap=np.zeros(int(np.multiply(SR, 0.25)))
song=np.concatenate([p1, gap, p2, gap, p3, gap])
song=np.tile(song, 3)
mx=np.max(np.abs(song))
song=np.multiply(np.divide(song, mx), 0.6)
song=np.multiply(song, 32767).astype(np.int16)
path=os.path.join(OUT, 'cat_meow.wav')
w=wave.open(path, 'w')
w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR)
w.writeframes(song.tobytes()); w.close()
print('WROTE', path, len(song)/SR)
