p = 'ops/content_video5.py'
s = open(p, encoding='utf-8').read()
# 1) VideoClip duration -> set via with_duration, then set_fps -> with_fps
old1 = 'vid = VideoClip(lambda t: mk(b.get_frame, t), duration=dur)'
new1 = 'vid = VideoClip(lambda t: mk(b.get_frame, t))'
old2 = 'return vid.set_fps(30)'
new2 = 'return vid.with_duration(dur).with_fps(30)'
old3 = 'aud = aud.subclipped(0, TARGET)'
new3 = 'aud = aud.subclipped(0, min(TARGET, aud.duration))'
for a, b in [(old1, new1), (old2, new2), (old3, new3)]:
 s = s.replace(a, b)
open(p, 'w', encoding='utf-8').write(s)
print('patched')
