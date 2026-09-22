# gen_vile.py - sinh anh 16:9 cho 5 video kenh ViLe Vi
import os, requests, time, sys
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
sys.path.insert(0, os.getcwd())
from ops.vile_content import VIDEOS
SCENES = [
	"wide establishing shot, cinematic composition",
	"dramatic close up, intense detail",
	"aerial view, epic scale",
	"side angle, scientific illustration style",
	"macro detail shot, extreme close up",
	"wide panorama, epic vista"]
for vid, cfg in VIDEOS.items():
	dst = "output/vile_" + vid
	os.makedirs(dst, exist_ok=True)
	base = cfg["prompt"]
	for i, scene in enumerate(SCENES):
		fn = dst + "/img" + str(i) + ".jpg"
		if os.path.exists(fn) and os.path.getsize(fn) > 5000:
			print(vid, i, "skip")
			continue
		p = base + ", " + scene + ", cinematic photography, 16:9 widescreen, ultra detailed, award winning"
		url = "https://image.pollinations.ai/prompt/" + requests.utils.quote(p) + "?width=1280&height=720&nologo=true&model=flux&seed=555&enhance=true"
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
			time.sleep(3)
		if not ok:
			print(vid, i, "FAILED")