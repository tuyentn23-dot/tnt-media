p = 'auto_youtube_bot_v2.py'
ls = open(p, encoding='utf-8').read().split(chr(10))
out = []
for ln in ls:
	if ln == '':
		out.append(ln)
		continue
	st = ln.lstrip(' ')
	lead = len(ln) - len(st)
	if lead == 0:
		out.append(ln)
	else:
		out.append(chr(9) * lead + st)
open(p, 'w', encoding='utf-8').write(chr(10).join(out))
print('done')
