import os, requests, time, sys
sys.stdout.reconfigure(encoding='utf-8', errors='replace')
CHAR = 'kawaii chibi gacha club character, 1girl, long pink hair with cat ears, big pink eyes with long lashes, black crop top, pink fluffy detached sleeves, pink skirt, pink boots, cat tail, pastel anime style, soft cel shading, pastel pink palette'
BG = 'scenic background green hills pink flowers blue sky clouds floating bubbles'
poses = {
	1: 'waving hand, warm smile, blushing',
	2: 'jumping happily, arms up, sparkling eyes'
}
for i, pose in poses.items():
	p = CHAR + ', ' + pose + ', ' + BG
	url = 'https://image.pollinations.ai/prompt/' + requests.utils.quote(p) + '?width=1024&height=1024&nologo=true&model=flux&seed=2024&enhance=true'
	ok = False
	for attempt in range(3):
		try:
			r = requests.get(url, timeout=120)
			if r.status_code == 200 and len(r.content) > 5000:
				fn = 'output/gacha_char/pose' + str(i) + '.jpg'
				open(fn, 'wb').write(r.content)
				print('pose', i, 'OK', len(r.content))
				ok = True
				break
			else:
				print('pose', i, 'attempt', attempt, 'status', r.status_code)
		except Exception as ex:
			print('pose', i, 'attempt', attempt, 'ERR', str(ex)[:60])
		time.sleep(3)
	if not ok:
		print('pose', i, 'FAILED ALL')