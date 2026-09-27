NL = chr(10)
p = 'app/server.py'
lines = open(p, encoding='utf-8').read().splitlines(keepends=True)

# Remove lines 219..243 (1-indexed) = indices 218..242
start = 218
end = 243 # exclusive
removed = lines[start:end]
assert removed[0].startswith("@app.post('/api/publications/{pub_id}/publish')"), removed[0]
new_lines = lines[:start] + lines[end:]
src = ''.join(new_lines)
open(p, 'w', encoding='utf-8').write(src)
import ast
ast.parse(src)
print('removed lines:', len(removed))
print('AST OK')
