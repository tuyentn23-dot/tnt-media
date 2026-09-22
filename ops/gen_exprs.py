import requests, os, time
os.makedirs('output/ai_anime', exist_ok=True)
base = 'masterpiece, best quality, anime style, 1girl, solo, long pink hair, purple eyes, black crop top, pink skirt, thigh highs, cel shading, full body, white background'
exprs = [
	'blushing, shy smile, looking away',
	'surprised, wide eyes, open mouth',
	'crying, tears, sad expression',
	'happy, big smile, sparkling eyes, arms up'
]
for i, e in enumerate(exprs):
	p = base + ', ' + e
	url = 'https://image.pollinations.ai/prompt/' + requests.utils.quote(p) + '?width=768&height=1024&nologo=true&model=flux&seed=42'
	try:
		r = requests.get(url, timeout=90)
		if r.status_code == 200 and len(r.content) > 5000:
			fn = 'output/ai_anime/expr' + str(i) + '.jpg'
			open(fn, 'wb').write(r.content)
			print('expr', i, 'OK', len(r.content))
		else:
			print('expr', i, 'FAIL', r.status_code)
	except Exception as ex:
		print('expr', i, 'ERR', str(ex)[:80])
	time.sleep(2)