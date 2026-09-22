import io
P='ops/control_center.py'
s=io.open(P,encoding='utf-8').read()
bad = '{\"channels\": [], \"active\": None}))'
good = '{\"channels\": [], \"active\": None})'
print('found:', bad in s)
if bad in s:
    s=s.replace(bad,good,1)
    io.open(P,'w',encoding='utf-8').write(s)
    import ast
    ast.parse(s)
    print('fixed + syntax OK')
