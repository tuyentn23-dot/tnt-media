import os, requests, time, sys
sys.stdout.reconfigure(encoding='utf-8', errors='replace')
os.makedirs('output/ai_anime', exist_ok=True)
base = 'masterpiece, best quality, ultra detailed, cute anime style, kawaii, chibi pikachu, yellow pokemon with red cheeks, big sparkling eyes, kawaii expression, pastel background with sparkles and stars, cel shading, vibrant soft colors, studio ghibli style, trending on pixiv, award winning illustration'
scenes = [
	'pikachu sitting happily waving paw, cute smile, pink pastel background',
	'pikachu jumping with joy, hearts floating around, rainbow sparkles background',
	'pikachu sleeping peacefully, fluffy clouds and stars, dreamy atmosphere',
	'pikachu holding a strawberry, blushing cheeks, flower garden background',
	'pikachu dancing with musical notes, cheerful vibes, bright colorful background',
	'pikachu surrounded by butterflies, magical glow, cherry blossom petals falling'
]
for i, scene in enumerate(scenes):
	p = base + ', ' + scene
	url = 'https://image.pollinations.ai/prompt/' + requests.utils.quote(p) + '?width=1024&height=1024&nologo=true&model=flux&seed=101&enhance=true'
	try:
		r = requests.get(url, timeout=120)
		if r.status_code == 200 and len(r.content) > 5000:
			fn = 'output/ai_anime/pika' + str(i) + '.jpg'
			open(fn, 'wb').write(r.content)
			print('pika', i, 'OK', len(r.content))
		else:
			print('pika', i, 'FAIL', r.status_code)
	except Exception as ex:
		print('pika', i, 'ERR', str(ex)[:80])
	time.sleep(1)