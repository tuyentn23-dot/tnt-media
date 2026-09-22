import requests, re, json
h = {"User-Agent": "Mozilla/5.0"}
r = requests.get('https://mixkit.co/free-stock-video/cat/', timeout=15, headers=h)
html = r.text
# tim contentUrl trong JSON-LD
urls = re.findall(r""contentUrl":"([^"]+)"", html)
print('CONTENT URLS:', len(urls))
for u in urls[:8]:
	print(u)
# fallback: assets.mixkit.co mp4
m2 = re.findall(r"https://assets[.]mixkit[.]co[^" ]*?[.]mp4", html)
print('ASSET MP4:', len(m2))
for u in m2[:8]:
	print(u)
