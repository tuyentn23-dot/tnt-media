import subprocess
r=subprocess.run(['node','--check','tools/_ui.js'], capture_output=True, text=True, encoding='utf-8', errors='replace')
lines=r.stderr.splitlines()
for l in lines:
    print(l.encode('ascii','replace').decode('ascii'))
