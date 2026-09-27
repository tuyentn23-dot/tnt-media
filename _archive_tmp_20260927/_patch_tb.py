import ast
U = chr(95); NL = chr(10); T = chr(9); Q = chr(39); DQ = chr(34)
p = 'pipeline/runner.py'
src = open(p, encoding='utf-8').read()
# Tim dong except trong build
old = 'except Exception as e:' + NL + T + T + T + "log('build FAIL: ' + str(e)[:120])"
new = 'except Exception as e:' + NL + T + T + T + 'import traceback' + NL + T + T + T + "log('build FAIL: ' + str(e)[:200])" + NL + T + T + T + 'log(traceback.format_exc()[-1500:])'
if old in src:
	src = src.replace(old, new, 1)
	print('patched build')
else:
	print('pattern not found')
open(p, 'w', encoding='utf-8').write(src)
ast.parse(src)
print('TB PATCH OK')
