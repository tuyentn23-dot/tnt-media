import requests
urls = ['https://mixkit.co/free-stock-video/cat/', 'https://www.pexels.com/search/videos/cat/']
h = {"User-Agent": "Mozilla/5.0"}
for u in urls:
	try:
		r = requests.get(u, timeout=10, headers=h)
		print(u, r.status_code, len(r.text))
	except Exception as e:
		print(u, 'ERR', str(e)[:80])
