import requests, re
h = {"User-Agent": "Mozilla/5.0"}
u = 'https://raw.githubusercontent.com/RayVentura/ShortGPT/stable/README.md'
txt = requests.get(u, timeout=15, headers=h).text
for kw in ['feature', 'workflow', 'engine', 'step']:
	i = txt.lower().find(kw)
	if i > 0:
		print('[' + kw + ']', txt[i:i+400].encode('ascii', 'replace').decode())
		print()
