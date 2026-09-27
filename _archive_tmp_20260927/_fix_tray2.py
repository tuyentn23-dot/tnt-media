p = 'app/tray.py'
NL = chr(10)
T1 = chr(9)
T3 = T1 + T1 + T1
T4 = T1 + T1 + T1 + T1
lines = open(p, encoding='utf-8').read().split(NL)
out = []
skip_until = None
for i, l in enumerate(lines):
	if l == T3 + 'try:' and i+1 < len(lines) and lines[i+1] == T4 + 'import msvcrt':
		out.append(T3 + 'try:')
		out.append(T4 + 'import msvcrt')
		out.append(T4 + 'msvcrt.locking(fd, msvcrt.LK_NBLCK, 1)')
		out.append(T3 + 'except Exception:')
		out.append(T4 + 'return None')
		out.append(T3 + 'return fd')
		skip_until = i + 7
		continue
	if skip_until is not None and i < skip_until:
		continue
	out.append(l)
open(p, 'w', encoding='utf-8', newline='').write(NL.join(out))
print('fixed lines', len(lines), '->', len(out))
