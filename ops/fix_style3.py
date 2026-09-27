p = 'ops/channel_style.py'
NL = chr(10)
T = chr(9)
T2 = T + T
T3 = T2 + T
T4 = T3 + T
Q = chr(39)
SP = chr(32)
lines = open(p, encoding='utf-8').read().split(NL)
start = None
for i, l in enumerate(lines):
	if l.startswith('def _wrap('):
		start = i
		break
if start is None:
	print('not found')
	sys.exit(1)
end = start + 1
while end < len(lines) and not (lines[end].startswith('def ') or lines[end].startswith('class ')):
	end += 1
new = [
	'def _wrap(draw, text, font, maxw):',
	T + 'words = text.split()',
	T + 'lines = []',
	T + 'cur = ' + Q + Q,
	T + 'for w in words:',
	T2 + 'test = (cur + ' + Q + SP + Q + ' + w).strip()',
	T2 + 'if draw.textlength(test, font=font) <= maxw:',
	T3 + 'cur = test',
	T2 + 'else:',
	T3 + 'if cur:',
	T4 + 'lines.append(cur)',
	T3 + 'cur = w',
	T + 'if cur:',
	T2 + 'lines.append(cur)',
	T + 'return lines',
	'',
	'',
]
out = lines[:start] + new + lines[end:]
open(p, 'w', encoding='utf-8', newline='').write(NL.join(out))
print('replaced', start, end, '->', len(out))
