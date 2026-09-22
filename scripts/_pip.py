import subprocess, sys
r=subprocess.run([sys.executable,'-m','pip','install','opencv-python-headless','pytesseract','easyocr'], capture_output=True, text=True)
print('RC', r.returncode)
print(r.stdout[-500:])
print(r.stderr[-500:])