# voice_synth.py - edge-tts natural speech (flat, no nested indent)
import os
import edge_tts
from ops import voice_engine as VE

def add_emotion(text):
	t = (text or '').strip()
	if not t:
		return t
	t = t.replace('. ', '. ... ')
	t = t.replace(', ', ', ')
	t = t.replace('? ', '? ... ')
	t = t.replace('! ', ' ! ')
	return t

def synth(text, out, voice='female_north', preset='hype', retries=5, maxlen=200):
	text = add_emotion((text or '')[:maxlen])
	v = VE.VI_VOICES.get(voice, voice)
	p = VE.PRESETS.get(preset, VE.PRESETS['hype'])
	import edge_tts, time, asyncio
	last = None
	for attempt in range(retries):
		try:
			c = edge_tts.Communicate(text, v, rate=p['rate'], pitch=p['pitch'], volume=p['volume'])
			VE._run(c.save(out))
			return out
		except Exception as e:
			last = e
			time.sleep(2.5)
	raise last

def synth_parts(parts, out, voice='female_north', preset='hype', gap=0.5):
	import subprocess
	from ops import voice_engine as VE
	segs = []
	for i, p in enumerate(parts):
		fp = out + '.p' + str(i) + '.mp3'
		synth(p, fp, voice=voice, preset=preset)
		segs.append(fp)
	sil = out + '.sil.mp3'
	subprocess.run([VE.FFMPEG, '-y', '-f', 'lavfi', '-i', 'anullsrc=r=24000:cl=mono', '-t', str(gap), sil], capture_output=True)
	order = []
	for s in segs:
		order.append(s)
		order.append(sil)
	order = order[:-1]
	import os
	lst = out + '.lst.txt'
	fh = open(lst, 'w', encoding='utf-8')
	for f in order:
		fh.write(chr(102)+chr(105)+chr(108)+chr(101)+chr(32)+chr(39)+os.path.abspath(f)+chr(39)+chr(10))
	fh.close()
	subprocess.run([VE.FFMPEG, '-y', '-f', 'concat', '-safe', '0', '-i', lst, '-c', 'copy', out], capture_output=True)
	return out

