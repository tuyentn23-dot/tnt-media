import sys
fn = sys.argv[1]
raw = open(fn, 'rb').read()
lines = raw.split(bytes([10]))
for i in [52, 53, 54, 88, 89, 90, 91, 92, 93]:
	if i - 1 < len(lines):
		print(i, lines[i-1])