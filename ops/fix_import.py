fn = 'ops/ffmpeg_render.py'
src = open(fn, encoding='utf-8').read()
lines = src.split(chr(10))
new_lines = []
removed = 0
for ln in lines:
	if ln == 'from ops import gacha_anime_render as GAR':
		removed += 1
		continue
	new_lines.append(ln)
src = chr(10).join(new_lines)
print('removed:', removed)
needle = chr(9) + 'from ops import gacha_sprite as G'
repl = needle + chr(10) + chr(9) + 'from ops import gacha_anime_render as GAR'
src = src.replace(needle, repl, 1)
open(fn, 'w', encoding='utf-8').write(src)
import ast
try:
	ast.parse(src)
	print('SYNTAX OK')
except SyntaxError as e:
	print('ERR:', e, 'line', e.lineno)