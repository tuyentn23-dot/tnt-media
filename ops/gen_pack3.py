import os, requests, time, sys, random
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
CHAR = "kawaii chibi gacha club character, 1girl, long pink hair with cat ears, big pink eyes, pastel anime style"
PACKS = {}
PACKS["cold"] = [
	"warm smile holding a heart, pink pastel background",
	"confused expression glitch effect, cracks in background",
	"serious cold expression, desaturated blue palette, snow falling",
	"icy blue eyes glowing, dark blue background ice crystals",
	"turning away from viewer, dark stormy background",
	"standing alone in snow with ice crown, melancholic"]
PACKS["wheel"] = [
	"magical pink outfit holding spinning wheel, sparkle background",
	"fantasy elf outfit, green forest background",
	"cyberpunk neon outfit, futuristic city background",
	"royal princess dress, castle background golden crown",
	"sporty casual outfit, school background dynamic pose",
	"magical girl outfit with wand, starry night background"]
PACKS["types"] = [
	"cute shy girl blushing holding book, school library",
	"cool confident girl with sunglasses, city street",
	"sporty energetic girl with ponytail running, track field",
	"artistic dreamy girl painting, art studio",
	"gamer girl with headset, neon room",
	"fashionista girl stylish pose, fashion runway"]
for pack, poses in PACKS.items():
	dst = "output/pack2_" + pack
	os.makedirs(dst, exist_ok=True)
	for i, pose in enumerate(poses):
		fn = dst + "/pose" + str(i) + ".jpg"
		if os.path.exists(fn) and os.path.getsize(fn) > 5000:
			print(pack, i, "skip")
			continue
		p = CHAR + ", " + pose
		seed = random.randint(1, 99999)
		url = "https://image.pollinations.ai/prompt/" + requests.utils.quote(p) + "?width=768&height=1024&nologo=true&model=flux&seed=" + str(seed)
		ok = False
		for att in range(4):
			try:
				r = requests.get(url, timeout=100)
				if r.status_code == 200 and len(r.content) > 5000:
					open(fn, "wb").write(r.content)
					print(pack, i, "OK", len(r.content))
					ok = True
					break
				else:
					print(pack, i, "att", att, "status", r.status_code)
			except Exception as ex:
				print(pack, i, "att", att, "err", str(ex)[:50])
			time.sleep(5)
		if not ok:
			print(pack, i, "FAILED")
		time.sleep(2)