# gen_gacha_char.py - sinh nhan vat Gacha cua Mia Linh Cute
import os, requests, time, sys
sys.stdout.reconfigure(encoding='utf-8', errors='replace')
os.makedirs('output/gacha_char', exist_ok=True)
# Prompt co dinh cho nhan vat - giong het anh user
CHAR = 'kawaii chibi gacha club character, 1girl, long pink hair with cat ears, big pink eyes with long lashes, black crop top, pink fluffy detached sleeves, pink skirt, pink boots, cat tail, pastel anime style, cute smile, soft cel shading, studio ghibli inspired, trending on pixiv, pastel pink color palette'
BG = 'scenic background with green hills, pink flowers, blue sky with clouds, floating bubbles, kawaii aesthetic'
poses = [
	'standing facing viewer, hands on hips, confident smile',
	'waving hand, warm smile, blushing',
	'jumping happily, arms up, sparkling eyes',
	'sitting on grass, hugging knees, cute pose',
	'twirling around, skirt flowing, joyful',
	'holding a pink heart, blushing shyly, looking away',
]
for i, pose in enumerate(poses):
	p = CHAR + ', ' + pose + ', ' + BG
	url = 'https://image.pollinations.ai/prompt/' + requests.utils.quote(p) + '?width=1024&height=1024&nologo=true&model=flux&seed=2024&enhance=true'
	try:
		r = requests.get(url, timeout=120)
		if r.status_code == 200 and len(r.content) > 5000:
			fn = 'output/gacha_char/pose' + str(i) + '.jpg'
			open(fn, 'wb').write(r.content)
			print('pose', i, 'OK', len(r.content))
		else:
			print('pose', i, 'FAIL', r.status_code)
	except Exception as ex:
		print('pose', i, 'ERR', str(ex)[:80])
	time.sleep(1)