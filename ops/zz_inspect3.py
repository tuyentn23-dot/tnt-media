import sys
fn = sys.argv[1]
raw = open(fn, 'rb').read()
lines = raw.split(bytes([10]))
for i, ln in enumerate(lines, 1):
	if b'name' in ln:
		print(i, ln)
