# gen_gacha_pack.py - sinh anh cho 4 video viral (3 video x 6 pose moi)
import os, requests, time, sys
sys.stdout.reconfigure(encoding='utf-8', errors='replace')
CHAR = 'kawaii chibi gacha club character, 1girl, long pink hair with cat ears, big pink eyes with long lashes, pink fluffy detached sleeves, cat tail, pastel anime style, soft cel shading, pastel pink palette, trending on pixiv'
# Pack 1: POV bullying/glow-up (ao den crop top -> vay cong chua)
# Pack 2: Water getting colder (am ap -> lanh lung, desaturated)
# Pack 3: Spin wheel OC (nhieu outfit khac nhau)
# Pack 4: Types of gacha girls (nhieu kieu toc/outfit)
PACKS = {
	'bully': [
		'black crop top pink skirt, standing alone looking sad, dark corridor background',
		'black crop top pink skirt, bullied by silhouette figures, rain and storm background',
		'black crop top pink skirt, crying with tears, gray gloomy background',
		'transformation, glowing pink light around body, magical aura',
		'princess pink dress with crown, confident smile, golden sparkle background',
		'princess dress, surrounded by adoring fans, bright celebration background'
	],
	'cold': [
		'warm smile, holding a heart, pink pastel background with flowers',
		'confused expression, cracks appearing in background, glitch effect',
		'serious cold expression, desaturated blue palette, snow falling',
		'icy blue eyes glowing, dark blue background with ice crystals',
		'turning away from viewer, cold shoulder, dark stormy background',
		'standing alone in snow, ice crown, melancholic atmosphere'
	],
	'wheel': [
		'magical pink outfit, holding a spinning wheel, sparkle background',
		'fantasy elf outfit, green forest background, pointy ears',
		'cyberpunk neon outfit, futuristic city background, holographic effects',
		'royal princess dress, castle background, golden crown',
		'sporty casual outfit, school background, dynamic pose',
		'magical girl outfit with wand, starry night background'
	],
	'types': [
		'cute shy girl, blushing, holding book, school library background',
		'cool confident girl, sunglasses, city street background',
		'sporty energetic girl, ponytail, running on track field',
		'artistic dreamy girl, painting, art studio background',
		'gamer girl, headset, neon room background',
		'fashionista girl, stylish pose, fashion runway background'
	]
}
for pack, poses in PACKS.items():
	os.makedirs('output/gacha_pack_' + pack, exist_ok=True)
	for i, pose in enumerate(poses):
		fn = 'output/gacha_pack_' + pack + '/pose' + str(i) + '.jpg'
		if os.path.exists(fn):
			print(pack, i, 'skip (exists)')
			continue
		p = CHAR + ', ' + pose
		url = 'https://image.pollinations.ai/prompt/' + requests.utils.quote(p) + '?width=1024&height=1024&nologo=true&model=flux&seed=2024&enhance=true'
		ok = False
		for attempt in range(3):
			try:
				r = requests.get(url, timeout=120)
				if r.status_code == 200 and len(r.content) > 5000:
					open(fn, 'wb').write(r.content)
					print(pack, i, 'OK', len(r.content))
					ok = True
					break
			except Exception as ex:
				print(pack, i, 'att', attempt, 'err', str(ex)[:50])
			time.sleep(2)
		if not ok:
			print(pack, i, 'FAILED')