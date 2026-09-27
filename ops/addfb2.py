p = 'ops/live_content.py'
src = open(p, encoding='utf-8').read()
NL = chr(10)
T = chr(9)
T2 = T + T
T3 = T2 + T
Q = chr(39)
Q3 = Q + Q
lines = [
	'',
	'',
	'FORBIDDEN_KW = [' + Q + 'hiếp dâm' + Q + ', ' + Q + 'cưỡng hiếp' + Q + ', ' + Q + 'tự tử' + Q + ', ' + Q + 'giết người' + Q + ', ' + Q + 'ma túy' + Q + ', ' + Q + 'đâm nhau' + Q + ']',
	'',
	'',
	'def is_forbidden(text):',
	T + 'low = (text or ' + Q3 + ').lower()',
	T + 'for k in FORBIDDEN_KW:',
	T2 + 'if k.lower() in low:',
	T3 + 'return True',
	T + 'return False',
	'',
	'',
	'def filter_items(items):',
	T + 'out = []',
	T + 'for it in items:',
	T2 + 'if is_forbidden(str(it.get(' + Q + 'hook' + Q + ', ' + Q3 + ')) + ' + Q + ' ' + Q + ' + str(it.get(' + Q + 'body' + Q + ', ' + Q3 + '))):',
	T3 + 'continue',
	T2 + 'out.append(it)',
	T + 'return out',
	'',
]
src = src + NL + NL + NL.join(lines)
open(p, 'w', encoding='utf-8', newline='').write(src)
print('appended functions')
