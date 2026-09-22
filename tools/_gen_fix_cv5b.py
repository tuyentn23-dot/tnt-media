p = 'ops/content_video5.py'
s = open(p, encoding='utf-8').read()
T = chr(9)
# replace import with wrapper that returns moviepy ColorClip directly (has crop/resize)
old = T + 'from ops.compat import color_clip as ColorClip'
new = (T + 'from ops.compat import _editor as _cmp_editor' + chr(10) +
 T + 'ColorClip = _cmp_editor()[5]')
if old in s:
 s = s.replace(old, new)
 open(p, 'w', encoding='utf-8').write(s)
 print('patched import')
else:
 print('NOT FOUND')
