p = 'ops/channel_style.py'
NL = chr(10)
T = chr(9)
src = open(p, encoding='utf-8').read()
lines = src.split(NL)
out = []
in_func = False
for l in lines:
	stripped = l.lstrip(' ')
	spaces = len(l) - len(stripped)
	# detect new function/class
	if l.startswith('def ') or l.startswith('class '):
		in_func = True
		out.append(l)
		continue
	if in_func and stripped:
		# convert leading spaces (1 space = 1 level in this file) to tabs
		out.append(T * spaces + stripped)
	else:
		out.append(l)
open(p, 'w', encoding='utf-8', newline='').write(NL.join(out))
print('done')
