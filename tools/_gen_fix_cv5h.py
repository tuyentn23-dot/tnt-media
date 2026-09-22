p = 'ops/content_video5.py'
s = open(p, encoding='utf-8').read()
# final cleanup: ensure order cropped BEFORE resized for ColorClip branch is fine, and remove duration kw from VideoClip call already done
# ensure 'with_duration' used on scenes concatenated
s = s.replace('vid = vid.set_audio(aud)', 'vid = vid.with_audio(aud)')
open(p, 'w', encoding='utf-8').write(s)
print('patched set_audio -> with_audio')
