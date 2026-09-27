import sys, subprocess, os
print('python exe:', sys.executable)
print('python version:', sys.version)
print('cwd:', os.getcwd())

r = subprocess.run([sys.executable, '-m', 'pip', 'install', '--quiet', 'imageio-ffmpeg', 'Pillow', 'python-dotenv'], capture_output=True, text=True)
print('pip rc:', r.returncode)
print('pip out:', (r.stdout or '')[-500:])
print('pip err:', (r.stderr or '')[-500:])

import importlib
for m in ['imageio_ffmpeg', 'PIL', 'dotenv']:
 try:
 importlib.invalidate_caches()
 importlib.import_module(m)
 print('OK', m)
 except Exception as e:
 print('MISSING', m, e)
