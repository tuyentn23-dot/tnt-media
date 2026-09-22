p = 'ops/channel_style.py'
s = open(p, encoding='utf-8').read()
T = chr(9)
old = T + T + 'from moviepy.editor import ImageClip, CompositeVideoClip'
new = T + T + 'from ops.compat import get_image_clip, composite'
old2 = T + T + 'wm_clip = ImageClip(overlay, duration=body.duration)'
new2 = T + T + 'wm_clip = get_image_clip()(overlay, duration=body.duration)'
old3 = T + T + 'body = CompositeVideoClip([body, wm_clip])'
new3 = T + T + 'body = composite([body, wm_clip])'
s = s.replace(old, new).replace(old2, new2).replace(old3, new3)
open(p, 'w', encoding='utf-8').write(s)
print('patched', 'moviepy.editor' not in s)
