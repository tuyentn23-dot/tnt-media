import subprocess, os, sys
os.chdir(os.path.abspath("."))
logf = open("output/pub_vile_log.txt", "w")
p = subprocess.Popen([sys.executable, "ops/pub_all_vile.py"], stdout=logf, stderr=subprocess.STDOUT, creationflags=0x00000008 | 0x00000200)
print("started pid", p.pid)