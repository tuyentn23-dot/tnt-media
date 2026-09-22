import os, requests, sys, time
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
sys.path.insert(0, os.getcwd())
from ops.mia_content_kids import VIDEOS
base = VIDEOS["pikachu_facts"]["char"]
pose = "sitting cute pose, vibrant colors, kid friendly, cute aesthetic"
p = base + ", " + pose
url = "https://image.pollinations.ai/prompt/" + requests.utils.quote(p) + "?width=768&height=1024&nologo=true&model=flux&seed=101&enhance=true"
fn = "output/mia_pikachu_facts/pose4.jpg"
for att in range(5):
	try:
		r = requests.get(url, timeout=120)
		if r.status_code == 200 and len(r.content) > 5000:
			open(fn, "wb").write(r.content)
			print("OK", len(r.content))
			break
		print("att", att, r.status_code)
	except Exception as e:
		print("err", str(e)[:60])
	time.sleep(3)