import subprocess, io
r=subprocess.run(['node','--check','tools/_ui.js'], capture_output=True, text=True, encoding='utf-8', errors='replace')
io.open('logs/node_err.txt','w',encoding='utf-8').write(r.stderr or '')
print('written len', len(r.stderr or ''))
# in dong co dau ^
for l in (r.stderr or '').splitlines():
    if '^' in l or 'SyntaxError' in l:
        print(repr(l))
