import sys
fn = sys.argv[1]
raw = open(fn, 'rb').read()
print('size bytes:', len(raw))
lines = raw.split(bytes([10]))
for i, ln in enumerate(lines[-8:], len(lines) - 7):
	print(i, ln)
