import requests, re
h = {"User-Agent": "Mozilla/5.0"}
r = requests.get('https://blog.youtube/inside-youtube/on-youtubes-recommendation-system/', timeout=15, headers=h)
txt = re.sub(r'<[^>]+>', ' ', r.text)
txt = re.sub(r'\s+', ' ', txt)
for kw in ['clickbait', 'watch time', 'satisfaction', 'survey', 'retention']:
	i = txt.lower().find(kw.lower())
	if i > 0:
		print('[' + kw + ']', txt[max(0,i-100):i+200].encode('ascii', 'replace').decode())
		print()
