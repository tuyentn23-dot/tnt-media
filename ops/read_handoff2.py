src = open('SESSION_HANDOFF.md', encoding='utf-8').read()
lines = src.split(chr(10))
for i, ln in enumerate(lines[435:499], 436):
	print(i, ln.encode('ascii', 'replace').decode('ascii'))