# gen_content_v2.py - sinh anh cho 4 video moi (meme/love/drama/cool)
import os, requests, time, sys
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
sys.path.insert(0, os.getcwd())
from ops.content_v2 import VIDEOS2
for vid, cfg in VIDEOS2.items():
	dst = "output/v2_" + vid
	os.makedirs(dst, exist_ok=True)
	char = cfg["char_prompt"]
	poses = [
		"standing confident, full body view",
		"close up face shot, emotional expression",
		"dynamic pose, arms crossed",
		"looking away, side view",
		"sitting down, thinking pose",
		"close up, dramatic expression"]
	for i, pose in enumerate(poses):
		fn = dst + "/pose" + str(i) + ".jpg"
		if os.path.exists(fn) and os.path.getsize(fn) > 5000:
			print(vid, i, "skip")
			continue
		p = char + ", " + pose + ", anime illustration, high quality, detailed, pastel colors"
		url = "https://image.pollinations.ai/prompt/" + requests.utils.quote(p) + "?width=768&height=1024&nologo=true&model=flux&seed=777&enhance=true"
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
				print(vid, i, "att", att, str(ex)[:50])
			time.sleep(3)
		if not ok:
			print(vid, i, "FAILED")