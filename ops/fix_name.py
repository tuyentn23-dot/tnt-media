# fix_name.py - sua loi write_file bien name thanh name
import sys
fn = sys.argv[1]
src = open(fn, encoding='utf-8').read()
bad = "if name == '" + chr(109) + "ain':"
good = "if " + chr(95) * 2 + "name" + chr(95) * 2 + " == '" + chr(95) * 2 + "main" + chr(95) * 2 + "':"
print('bad pattern repr:', repr(bad))
print('found bad?', bad in src)
print('count bad:', src.count(bad))
if bad in src:
	src = src.replace(bad, good)
	with open(fn, 'w', encoding='utf-8') as f:
		f.write(src)
	print('FIXED', fn)
else:
	# thu pattern khac: co the la 		if name == ...
	bad2 = "name == '" + chr(109) + "ain'"
	good2 = chr(95) * 2 + "name" + chr(95) * 2 + " == '" + chr(95) * 2 + "main" + chr(95) * 2 + "'"
	print('count bad2 (substring):', src.count(bad2))
	if bad2 in src:
		src = src.replace(bad2, good2)
		with open(fn, 'w', encoding='utf-8') as f:
			f.write(src)
		print('FIXED (substring)', fn)
