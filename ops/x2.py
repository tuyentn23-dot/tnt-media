src = open('ops/build_pika_mv2.py', encoding='utf-8').read()
lines = src.split(chr(10))
for i, ln in enumerate(lines):
	if 'ff = ' in ln and 'FONT' in ln:
		print(i + 1, repr(ln))
	if 'tf = fp' in ln:
		print(i + 1, repr(ln))