# gan_pack_fallback.py - gan pack cold/wheel/types dung gacha_char neu thieu anh
import os, shutil
PACKS = ["cold", "wheel", "types"]
SRC = "output/gacha_char"
for pack in PACKS:
	dst_dir = "output/gacha_pack_" + pack
	os.makedirs(dst_dir, exist_ok=True)
	existing = sorted([f for f in os.listdir(dst_dir) if f.startswith("pose")] if os.path.isdir(dst_dir) else [])
	print(pack, "existing:", existing)
	for i in range(6):
		fn = dst_dir + "/pose" + str(i) + ".jpg"
		if os.path.exists(fn) and os.path.getsize(fn) > 5000:
			continue
		src = SRC + "/pose" + str(i) + ".jpg"
		if os.path.exists(src):
			shutil.copy(src, fn)
			print(pack, i, "copied from gacha_char")
		else:
			print(pack, i, "MISSING")
print("DONE")