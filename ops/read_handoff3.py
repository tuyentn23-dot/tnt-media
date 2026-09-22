src = open('SESSION_HANDOFF.md', encoding='utf-8').read()
lines = src.split(chr(10))
out = []
for i, ln in enumerate(lines[443:499], 444):
	out.append(str(i) + ' ' + ln.encode('ascii', 'replace').decode('ascii'))
print(chr(10).join(out))