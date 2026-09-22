import requests
h = {"User-Agent": "Mozilla/5.0"}
urls = [
	'https://www.youtube.com/howyoutubeworks/',
	'https://support.google.com/youtube/answer/11914225',
	'https://blog.youtube/inside-youtube/on-youtubes-recommendation-system/',
]
for u in urls:
	try:
		r = requests.get(u, timeout=15, headers=h)
		print(u, r.status_code, len(r.text))
	except Exception as e:
		print(u, 'ERR', str(e)[:50])
