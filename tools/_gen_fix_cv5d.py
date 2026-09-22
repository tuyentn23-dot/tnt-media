p = 'ops/content_video5.py'
s = open(p, encoding='utf-8').read()
s = s.replace('.subclip(', '.subclipped(')
open(p, 'w', encoding='utf-8').write(s)
print('done')
