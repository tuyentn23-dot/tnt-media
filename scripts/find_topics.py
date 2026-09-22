import requests, re
h = {"User-Agent": "Mozilla/5.0"}
tags = ['soccer', 'football', 'dog', 'funny']
for tg in tags:
	try:
		r = requests.get('https://mixkit.co/free-stock-video/' + tg + '/', timeout=15, headers=h)
		cnt = r.text.count('assets.mixkit.co/videos')
		urls = re.findall(r'https://assets[.]mixkit[.]co/videos/[0-9]+/[0-9-]+[.]mp4', r.text)
		uniq = list(dict.fromkeys(urls))
		print(tg, r.status_code, 'urls:', len(uniq), uniq[:3])
	except Exception as e:
		print(tg, 'ERR', str(e)[:60])
