import requests, os, time
os.makedirs('output/ai_anime', exist_ok=True)
base = 'masterpiece, best quality, ultra detailed, anime style, 1girl, solo, long pink hair, purple eyes, black crop top, pink skirt, thigh highs, cute smile, standing, full body, white background, cel shading, vibrant colors'
# 4 poses khac nhau (dung seed khac nhau de giu nhan vat tuong tu)
poses = [
	'standing facing viewer, arms at sides',
	'standing, one hand waving, slight smile',
	'standing, hands on hips, confident pose',
	'standing, eyes closed, gentle smile'
]
for model in ['flux', 'sana']:
	for i, pose in enumerate(poses):
		p = base + ', ' + pose
		url = 'https://image.pollinations.ai/prompt/' + requests.utils.quote(p) + '?width=768&height=1024&nologo=true&model=' + model + '&seed=42'
		try:
			r = requests.get(url, timeout=90)
			ok = r.status_code == 200 and len(r.content) > 5000
			if ok:
				fn = 'output/ai_anime/' + model + '_pose' + str(i) + '.jpg'
				open(fn, 'wb').write(r.content)
				print(model, i, 'OK', len(r.content))
			else:
				print(model, i, 'FAIL', r.status_code)
		except Exception as e:
			print(model, i, 'ERR', str(e)[:80])
		time.sleep(2)