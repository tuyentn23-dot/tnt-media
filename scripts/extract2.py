import requests, re
h = {"User-Agent": "Mozilla/5.0"}
r = requests.get('https://support.google.com/youtube/answer/11914225', timeout=15, headers=h)
txt = re.sub('<script[^>]>.?</script>', ' ', r.text, flags=re.S)
txt = re.sub('<[^>]+>', ' ', txt)
txt = re.sub(' +', ' ', txt)
for kw in ['viewer', 'watch', 'satisf', 'survey']:
	i = txt.lower().find(kw)
	if i > 0:
		print(kw, '::', txt[max(0,i-120):i+250].encode('ascii', 'replace').decode())
		print()
