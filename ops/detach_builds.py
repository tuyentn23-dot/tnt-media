import subprocess, os, sys
os.chdir(os.path.abspath("."))
vids = ["moon", "shark", "brain", "heart"]
for v in vids:
 logf = open("output/detach_" + v + ".txt", "w")
 p = subprocess.Popen(
 [sys.executable, "ops/build_vile.py", v],
 stdout=logf, stderr=subprocess.STDOUT,
 creationflags=0x00000008 | 0x00000200
 )
 print(v, "started pid", p.pid)
print("ALL DETACHED")