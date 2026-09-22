import requests
h = {"User-Agent": "Mozilla/5.0"}
u = 'https://raw.githubusercontent.com/RayVentura/ShortGPT/stable/README.md'
txt = requests.get(u, timeout=15, headers=h).text
i = txt.find('Engine')
print(txt[i:i+1800].encode('ascii', 'replace').decode())
