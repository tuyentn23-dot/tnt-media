import requests, re
h = {"User-Agent": "Mozilla/5.0"}
r = requests.get('https://mixkit.co/free-stock-video/cat/', timeout=15, headers=h)
html = r.text
# tim .mp4 hoac video url bat ky
for pat in ['mp4', 'video', 'assets']:
	idx = html.lower().find(pat)
	print(pat, idx, repr(html[max(0,idx-60):idx+60]))
