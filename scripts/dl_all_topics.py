import requests, json, os
h = {"User-Agent": "Mozilla/5.0"}
db = json.load(open('analytics/video_sources.json'))
base = 'content/assets/videos'
os.makedirs(base, exist_ok=True)
for topic, urls in db.items():
	odir = os.path.join(base, topic)
	os.makedirs(odir, exist_ok=True)
	for u in urls:
		vid = u.split('/')[-2]
		p = os.path.join(odir, vid + '.mp4')
		if os.path.exists(p) and os.path.getsize(p) > 100000:
			print('skip', topic, vid)
			continue
		try:
			r = requests.get(u, timeout=90, headers=h, stream=True)
			with open(p, 'wb') as f:
				for ch in r.iter_content(65536):
					f.write(ch)
			print('OK', topic, vid, os.path.getsize(p))
		except Exception as e:
			print('ERR', u, str(e)[:60])
print('DONE ALL')
