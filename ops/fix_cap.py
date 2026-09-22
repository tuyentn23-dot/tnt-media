fn = 'ops/build_gacha_viral.py'
src = open(fn, encoding='utf-8').read()
# Doi os.path.join(cap_tmp, ...) thanh cap_tmp + chr(47) + ...
old = chr(34) + chr(9) + 'fp = os.path.join(cap_tmp, ' + chr(39) + 'c%d.txt' + chr(39) + ' % k)' + chr(34)
new = chr(34) + chr(9) + 'fp = cap_tmp + chr(47) + (' + chr(39) + 'c%d.txt' + chr(39) + ' % k)' + chr(34)
print('found:', old in src)
src = src.replace(old, new, 1)
open(fn, 'w', encoding='utf-8').write(src)
print('done')