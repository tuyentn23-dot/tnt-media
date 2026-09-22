p = 'ops/content_video5.py'
s = open(p, encoding='utf-8').read()
T = chr(9)
lines = s.split(chr(10))
out = []
i = 0
n = len(lines)
while i < n:
	l = lines[i]
	out.append(l)
	if ('from ops.compat import _editor as _cmp_editor' in l) and (i + 1 < n) and ('ColorClip = _cmp_editor()[5]' in lines[i + 1]):
		out.append(lines[i + 1])
		out.append(T + 'VideoClip = _cmp_editor()[0]')
		i = i + 2
		continue
	i = i + 1
open(p, 'w', encoding='utf-8').write(chr(10).join(out))
print('patched VideoClip import')
