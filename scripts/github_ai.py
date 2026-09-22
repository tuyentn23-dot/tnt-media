import requests, json
h = {"User-Agent": "Mozilla/5.0"}
# Tim repo GitHub ve AI youtube automation
qs = ['youtube+shorts+automation+ai', 'faceless+youtube+ai', 'youtube+bot+upload+ai']
for q in qs:
	try:
		u = 'https://api.github.com/search/repositories?q=' + q + '&sort=stars&per_page=5'
		r = requests.get(u, timeout=15, headers=h)
		d = r.json()
		print('Q:', q)
		for it in d.get('items', [])[:5]:
			print(it['stargazers_count'], it['full_name'], (it['description'] or '')[:60].encode('ascii', 'replace').decode())
	except Exception as e:
		print(q, 'ERR', str(e)[:50])
