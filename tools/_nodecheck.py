import subprocess
r=subprocess.run(['node','--check','tools/_ui.js'], capture_output=True, text=True, encoding='utf-8', errors='replace')
print('RC', r.returncode)
print(r.stderr[-1500:])
