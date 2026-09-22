import sys, os
sys.stdout.reconfigure(encoding="utf-8")
os.chdir('D:/TNT_AI/venture_foundry/media')
sys.path.insert(0, 'D:/TNT_AI/venture_foundry/media')
import ops.music_gen as MG
moods = ['chill', 'energetic']
bpms = [70, 80, 90, 100, 110, 120]
n = 0
for seed in range(220):
	mood = moods[seed % 2]
	bpm = bpms[seed % len(bpms)]
	out = 'music_bank/m' + str(seed).zfill(3) + '.wav'
	try:
		MG.gen_track(out, seed=seed, dur=25, bpm=bpm, mood=mood)
		n += 1
	except Exception:
		pass
print('GENERATED', n)
