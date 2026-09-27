import ast
U = chr(95); NL = chr(10)
p = 'ops/content' + U + 'video5.py'
L = open(p, encoding='utf-8').read().split(NL)
start = None
end = None
for i, l in enumerate(L):
	if l.startswith('def make' + U + 'scene('):
		start = i
	if start is not None and l.startswith('def tts('):
		end = i
		break
print('block', (start or 0) + 1, '-', (end or 0) + 1)
if start is not None and end is not None:
	new_func = open('ops/' + U + 'append' + U + 'ms2.py', encoding='utf-8').read().split(NL)
	new_L = L[:start] + new_func + [NL] + L[end:]
	content = NL.join(new_L)
	open(p, 'w', encoding='utf-8').write(content)
	try:
		ast.parse(content)
		print('REPLACE2 OK, lines:', len(new_L))
	except Exception as e:
		print('ERR:', e)
