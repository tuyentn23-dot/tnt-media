import ast
U = chr(95); NL = chr(10); T = chr(9); Q = chr(39); DQ = chr(34)
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
print('block', start + 1 if start else 'NF', '-', end + 1 if end else 'NF')
if start is not None and end is not None:
	new_func = open('ops/' + U + 'append' + U + 'ms.py', encoding='utf-8').read().split(NL)
	new_L = L[:start] + new_func + [NL] + L[end:]
	content = NL.join(new_L)
	open(p, 'w', encoding='utf-8').write(content)
	try:
		ast.parse(content)
		print('REPLACE OK, lines:', len(new_L))
	except Exception as e:
		print('ERR:', e)
