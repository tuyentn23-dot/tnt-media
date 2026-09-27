p = 'app/tray.py'
NL = chr(10)
T = chr(9)
T2 = T + T
T3 = T2 + T
T4 = T3 + T
lines = open(p, encoding='utf-8').read().split(NL)
out = []
i = 0
while i < len(lines):
	l = lines[i]
	if l == T2 + 'try:' and i+1 < len(lines) and lines[i+1] == T3 + 'import msvcrt':
		out.append(T2 + 'try:')
		out.append(T3 + 'import msvcrt')
		out.append(T3 + 'msvcrt.locking(fd, msvcrt.LK_NBLCK, 1)')
		out.append(T2 + 'except Exception:')
		out.append(T3 + 'return None')
		out.append(T2 + 'return fd')
		i += 7
		continue
	out.append(l)
	i += 1
open(p, 'w', encoding='utf-8', newline='').write(NL.join(out))
print('done', len(lines), '->', len(out))
