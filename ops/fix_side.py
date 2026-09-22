U = '_'
fn = 'ops/gacha_anime_final.py'
src = open(fn, encoding='utf-8').read()
pairs = ['shoulder', 'elbow', 'wrist', 'hip', 'knee', 'ankle']
n = 0
for p in pairs:
	bad = chr(39) + p + chr(39) + ' + side'
	good = chr(39) + p + U + chr(39) + ' + side'
	c = src.count(bad)
	if c:
		src = src.replace(bad, good)
		n += c
		print('fixed', p, c)
open(fn, 'w', encoding='utf-8').write(src)
print('total', n)