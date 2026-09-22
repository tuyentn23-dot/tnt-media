p = 'ops/content_video5.py'
s = open(p, encoding='utf-8').read()
lines = s.split(chr(10))
out = [l for l in lines if 'fl_image' not in l]
open(p, 'w', encoding='utf-8').write(chr(10).join(out))
print('done', len(lines) - len(out))
