p = 'auto_youtube_bot_v2.py'
lines = open(p, encoding='utf-8').read().split(chr(10))
out = []
for ln in lines:
	if ln == '':
		out.append(ln)
		continue
	st = ln.lstrip(' ')
	lead = len(ln) - len(st)
	if lead == 1:
		out.append(' ' + st)
	elif lead == 2:
		out.append(' ' + st)
	else:
		out.append(ln)
open(p, 'w', encoding='utf-8').write(chr(10).join(out))
print('ok')
