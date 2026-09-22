import requests
h = {"User-Agent": "Mozilla/5.0"}
# Lay README cua ShortGPT
u = 'https://raw.githubusercontent.com/RayVentura/ShortGPT/main/README.md'
r = requests.get(u, timeout=15, headers=h)
print('STATUS:', r.status_code)
print(r.text[:1200].encode('ascii', 'replace').decode())
