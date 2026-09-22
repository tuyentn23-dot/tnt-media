import requests, os
h = {"User-Agent": "Mozilla/5.0"}
url = 'https://assets.mixkit.co/videos/1779/1779-1080.mp4'
os.makedirs('content/assets/cat_videos', exist_ok=True)
r = requests.get(url, timeout=60, headers=h, stream=True)
p = 'content/assets/cat_videos/cat_1779.mp4'
with open(p, 'wb') as f:
	for chunk in r.iter_content(65536):
		f.write(chunk)
print('DOWNLOADED', p, os.path.getsize(p))
