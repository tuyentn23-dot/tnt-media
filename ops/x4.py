fn = 'ops/build_gacha_viral.py'
src = open(fn, encoding='utf-8').read()
# Sua dong fp = os.path.join(cap_tmp, cN.txt) thanh dung
bad = chr(39) + 'fp = os.path.join(cap_tmp, ' + chr(39) + '%d.txt' + chr(39) + ' % k)' + chr(39)
print('searching...')
lines = src.split(chr(10))
for i, ln in enumerate(lines):
	if 'os.path.join(cap_tmp' in ln:
		print(i + 1, repr(ln))