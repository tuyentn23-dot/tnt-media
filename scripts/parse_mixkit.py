import requests, re
h = {"User-Agent": "Mozilla/5.0"}
r = requests.get('https://mixkit.co/free-stock-video/cat/', timeout=15, headers=h)
html = r.text
# Tim URL video mp4
mp4 = re.findall(r"https://[^""]*?[.]mp4", html)
print('FOUND MP4:', len(mp4))
for m in mp4[:10]:
	print(m)
