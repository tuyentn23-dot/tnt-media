import requests, os, time
h = {"User-Agent": "Mozilla/5.0"}
urls = [
	'https://assets.mixkit.co/videos/22732/22732-1080.mp4',
	'https://assets.mixkit.co/videos/1778/1778-1080.mp4',
	'https://assets.mixkit.co/videos/9949/9949-720.mp4',
	'https://assets.mixkit.co/videos/49058/49058-720.mp4',
]
os.makedirs('content/assets/cat_videos', exist_ok=True)
for u in urls:
	name = u.split('/')[-2] + '.mp4'
	p = os.path.join('content/assets/cat_videos', 'cat_' + name)
	if os.path.exists(p):
		print('skip', p)
		continue
	try:
		r = requests.get(u, timeout=90, headers=h, stream=True)
		with open(p, 'wb') as f:
			for ch in r.iter_content(65536):
				f.write(ch)
		print('OK', p, os.path.getsize(p))
	except Exception as e:
		print('ERR', u, str(e)[:80])
