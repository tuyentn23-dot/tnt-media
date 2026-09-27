import io, sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
d = open('app/_routes_publish.py', encoding='utf-8').read()
for i, l in enumerate(d.split(chr(10)), 1):
	if 'force' in l or 'publish(' in l:
		print(i, l)
