import ast, os, tempfile
p = 'ops/ffmpeg_render.py'
src = open(p, encoding='utf-8').read()
NL = chr(10)
TB = chr(9)
SP = chr(32)
SP4 = SP+SP+SP+SP
SP8 = SP4+SP4

# --- Patch 1: line with tab indent ---
old1 = TB + "tmp = '_work'; os.makedirs(tmp, exist_ok=True)"
new1 = TB + "base = os.path.join(ROOT, 'work')" + NL + TB + "os.makedirs(base, exist_ok=True)" + NL + TB + "tmp = tempfile.mkdtemp(prefix='render', dir=base)"

# --- Patch 2: line with 8-space indent ---
old2 = SP8 + "tmp = '_work'; os.makedirs(tmp, exist_ok=True)"
new2 = SP8 + "base = os.path.join(ROOT, 'work')" + NL + SP8 + "os.makedirs(base, exist_ok=True)" + NL + SP8 + "tmp = tempfile.mkdtemp(prefix='render', dir=base)"

n = 0
if old1 in src:
 src = src.replace(old1, new1, 1); n += 1
if old2 in src:
 src = src.replace(old2, new2, 1); n += 1

# ensure tempfile imported
top = 'import os'
if 'import tempfile' not in src:
 src = src.replace('import hashlib', 'import hashlib' + NL + 'import tempfile', 1)

open(p, 'w', encoding='utf-8').write(src)
print('patched:', n)
ast.parse(open(p, encoding='utf-8').read())
print('AST OK')
