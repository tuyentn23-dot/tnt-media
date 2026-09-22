import requests, re, json
h = {"User-Agent": "Mozilla/5.0"}
r = requests.get('https://mixkit.co/free-stock-video/cat/', timeout=15, headers=h)
html = r.text
key = "contentUrl"
i = 0
found = []
while True:
	i = html.find(key, i)
	if i < 0:
		break
	seg = html[i:i+300]
	m = re.search('https://[^"]+[.]mp4', seg)
	if m:
		found.append(m.group(0))
	i += 1
print('FOUND:', len(found))
for u in found[:8]:
	print(u)
