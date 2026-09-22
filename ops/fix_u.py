import sys
U = bytes([95, 95])
fn = sys.argv[1]
raw = open(fn, 'rb').read()
bad1 = b'os.path.abspath(file)'
good1 = b'os.path.abspath(' + U + b'file' + U + b')'
bad2 = b'if name == ' + bytes([39]) + b'main' + bytes([39]) + b':'
good2 = b'if ' + U + b'name' + U + b' == ' + bytes([39]) + U + b'main' + U + bytes([39]) + b':'
n = 0
if bad1 in raw:
 raw = raw.replace(bad1, good1); n += 1
if bad2 in raw:
 raw = raw.replace(bad2, good2); n += 1
open(fn, 'wb').write(raw)
print('fixed', n)