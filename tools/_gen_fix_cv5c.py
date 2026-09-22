p = 'ops/content_video5.py'
s = open(p, encoding='utf-8').read()
repls = [
 ('.crop(width=720, x_center=b.w/2)', '.cropped(width=720, x_center=b.w/2)'),
 ('.crop(width=720, height=1280, x_center=b.w/2, y_center=b.h/2)', '.cropped(width=720, height=1280, x_center=b.w/2, y_center=b.h/2)'),
 ('.resize(height=1280)', '.resized(height=1280)'),
 ('.resize(width=720)', '.resized(width=720)'),
]
for a, b in repls:
 s = s.replace(a, b)
open(p, 'w', encoding='utf-8').write(s)
print('done')
