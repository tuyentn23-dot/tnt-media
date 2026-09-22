p = 'ops/content_video5.py'
s = open(p, encoding='utf-8').read()
T = chr(9)
old = T + 'from moviepy.editor import ColorClip, VideoClip'
new = T + 'from ops.compat import color_clip as ColorClip'
s = s.replace(old, new)
open(p, 'w', encoding='utf-8').write(s)
print('patched', 'moviepy.editor' not in s)
