src = open('SESSION_HANDOFF.md', encoding='utf-8').read()
lines = src.split(chr(10))
print('total:', len(lines))
start = None
for i, ln in enumerate(lines):
	if 'DANG VIDEO' in ln or 'DANG BAI' in ln:
		start = i
		break
print('start:', start)