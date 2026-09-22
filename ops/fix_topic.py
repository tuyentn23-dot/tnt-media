fn = 'ops/channel_render.py'
src = open(fn, encoding='utf-8').read()
old = "topic = (item.get('topic') or '').lower()"
new = "topic = (item.get('topic') or '').lower() or ((item.get('id') or '').split(chr(95))[0].lower())"
print('found:', src.count(old))
src = src.replace(old, new, 1)
open(fn, 'w', encoding='utf-8').write(src)
import ast
try:
	ast.parse(src)
	print('SYNTAX OK')
except SyntaxError as e:
	print('ERR', e)