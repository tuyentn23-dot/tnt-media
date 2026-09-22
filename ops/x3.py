src = open('ops/build_pika_mv2.py', encoding='utf-8').read()
lines = src.split(chr(10))
for i, ln in enumerate(lines, 1):
	if 'silent2' in ln or 'pika_frames2' in ln or '_pika_caps' in ln:
		print(i, repr(ln))