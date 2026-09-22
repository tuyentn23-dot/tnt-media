import os, requests, time, sys
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
CHAR = "kawaii chibi gacha club character, 1girl, long pink hair with cat ears, big pink eyes with long lashes, pink fluffy detached sleeves, cat tail, pastel anime style, soft cel shading"
PACKS = {}
PACKS["cold"] = ["warm smile, holding a heart, pink pastel background", "confused expression, glitch effect, cracks in background", "serious cold expression, desaturated blue palette, snow falling", "icy blue eyes glowing, dark blue background, ice crystals", "turning away from viewer, dark stormy background", "standing alone in snow, ice crown, melancholic atmosphere"]
PACKS["wheel"] = ["magical pink outfit, holding a spinning wheel, sparkle background", "fantasy elf outfit, green forest background, pointy ears", "cyberpunk neon outfit, futuristic city background", "royal princess dress, castle background, golden crown", "sporty casual outfit, school background, dynamic pose", "magical girl outfit with wand, starry night background"]
PACKS["types"] = ["cute shy girl, blushing, holding book, school library background", "cool confident girl, sunglasses, city street background", "sporty energetic girl, ponytail, running on track field", "artistic dreamy girl, painting, art studio background", "gamer girl, headset, neon room background", "fashionista girl, stylish pose, fashion runway background"]
for pack, poses in PACKS.items():
	os.makedirs("output/gacha_pack_" + pack, exist_ok=True)
	for i, pose in enumerate(poses):
		fn = "output/gacha_pack_" + pack + "/pose" + str(i) + ".jpg"
		if os.path.exists(fn) and os.path.getsize(fn) > 5000:
			print(pack, i, "skip")
			continue
		p = CHAR + ", " + pose
		url = "https://image.pollinations.ai/prompt/" + requests.utils.quote(p) + "?width=1024&height=1024&nologo=true&model=flux&seed=2024&enhance=true"
		try:
			r = requests.get(url, timeout=90)
			if r.status_code == 200 and len(r.content) > 5000:
				open(fn, "wb").write(r.content)
				print(pack, i, "OK", len(r.content))
			else:
				print(pack, i, "FAIL", r.status_code)
		except Exception as ex:
			print(pack, i, "ERR", str(ex)[:50])
		time.sleep(1)