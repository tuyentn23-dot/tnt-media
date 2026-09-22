import requests
h = {"User-Agent": "Mozilla/5.0"}
r = requests.get('https://api.github.com/repos/RayVentura/ShortGPT', timeout=15, headers=h)
d = r.json()
print('BRANCH:', d.get('default_branch'))
print('DESC:', (d.get('description') or '').encode('ascii', 'replace').decode())
print('TOPICS:', d.get('topics'))
br = d.get('default_branch', 'main')
u = 'https://raw.githubusercontent.com/RayVentura/ShortGPT/' + br + '/README.md'
r2 = requests.get(u, timeout=15, headers=h)
print('README STATUS:', r2.status_code)
print(r2.text[:1500].encode('ascii', 'replace').decode())
