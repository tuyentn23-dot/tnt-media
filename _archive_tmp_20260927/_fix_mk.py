import ast
U = chr(95); NL = chr(10); T = chr(9); Q = chr(39); DQ = chr(34)
p = 'ops/content' + U + 'video5.py'
L = open(p, encoding='utf-8').read().split(NL)
start = None
end = None
for i, l in enumerate(L):
	if l.strip() == 'def mk(get, t):':
		start = i
	if start is not None and 'vid = VideoClip' in l:
		end = i
		break
print('mk block', (start or 0) + 1, '-', (end or 0) + 1)
if start is not None and end is not None:
	new_mk = [
		T + 'def mk(get, t):',
		T + T + 'try:',
		T + T + T + 'fr = get(t)',
		T + T + 'except Exception:',
		T + T + T + 'fr = np.zeros((1280, 720, 3), dtype=np.uint8)',
		T + T + 'if fr.dtype != np.uint8:',
		T + T + T + 'fr = fr.astype(np.uint8)',
		T + T + 'img = Image.fromarray(fr)',
		T + T + 'if img.mode != ' + DQ + 'RGB' + DQ + ':',
		T + T + T + 'img = img.convert(' + DQ + 'RGB' + DQ + ')',
		T + T + 'if img.size != (720, 1280):',
		T + T + T + 'img = img.resize((720, 1280), Image.LANCZOS)',
		T + T + 'img.paste(overlay, (0, 0), overlay)',
		T + T + 'return np.asarray(img, dtype=np.uint8)',
	]
	new_L = L[:start] + new_mk + L[end:]
	content = NL.join(new_L)
	open(p, 'w', encoding='utf-8').write(content)
	try:
		ast.parse(content)
		print('MK PATCH OK, lines:', len(new_L))
	except Exception as e:
		print('ERR:', e)
