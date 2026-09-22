# gen_mia_kids.py - sinh anh 9:16 cho 5 video kenh Mia (kids content)
import os, requests, time, sys
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
sys.path.insert(0, os.getcwd())
from ops.mia_content_kids import VIDEOS
POSES = [
	"standing happy, cheerful pose",
	"close up face, big expressive eyes",
	"jumping with joy, dynamic pose",
	"side view, looking curious",
	"sitting cute pose",
	"action pose, energetic"]
for vid, cfg in VIDEOS.items():
	dst = "output/mia_" + vid
	os.makedirs(dst, exist_ok=True)
	base = cfg["char"]
	for i, pose in enumerate(POSES):
		fn = dst + "/pose" + str(i) + ".jpg"
		if os.path.exists(fn) and os.path.getsize(fn) > 5000:
			print(vid, i, "skip")
			continue
		p = base + ", " + pose + ", vibrant colors, kid friendly, high quality, cute aesthetic"
		url = "https://image.pollinations.ai/prompt/" + requests.utils.quote(p) + "?width=768&height=1024&nologo=true&model=flux&seed=101&enhance=true"
		ok = False
		for att in range(3):
			try:
				r = requests.get(url, timeout=100)
				if r.status_code == 200 and len(r.content) > 5000:
					open(fn, "wb").write(r.content)
					print(vid, i, "OK", len(r.content))
					ok = True
					break
			except Exception as ex:
				print(vid, i, "err", str(ex)[:50])
			time.sleep(2)
		if not ok:
			print(vid, i, "FAIL")