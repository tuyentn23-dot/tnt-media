import requests, re, json
h = {"User-Agent": "Mozilla/5.0"}
tags = ['soccer', 'dog', 'funny', 'baby', 'nature', 'dance']
db = {}
for tg in tags:
	try:
		r = requests.get('https://mixkit.co/free-stock-video/' + tg + '/', timeout=15, headers=h)
		urls = re.findall(r'https://assets[.]mixkit[.]co/videos/[0-9]+/[0-9]+-1080[.]mp4', r.text)
		db[tg] = list(dict.fromkeys(urls))[:8]
		print(tg, len(db[tg]))
	except Exception as e:
		print(tg, 'ERR', str(e)[:60])
json.dump(db, open('analytics/video_sources.json', 'w'))
print('saved')
