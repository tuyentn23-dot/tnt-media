import os, re
out=[]
pats=["sys.executable","python.exe","pythonw","os.popen","os.spawn","Popen(","subprocess.call","subprocess.check"]
for root,dirs,files in os.walk("."):
	dirs[:]=[d for d in dirs if d not in ("pycache",".git","_archive_tmp_20260927","_archive_root_20260927","backups","node_modules","logs")]
	for f in files:
		if not f.endswith(".py"): continue
		fp=os.path.join(root,f)
		try: t=open(fp,encoding="utf-8",errors="replace").read()
		except: continue
		for i,l in enumerate(t.split(chr(10))):
			if any(p in l for p in pats):
				out.append(fp+chr(58)+str(i+1)+chr(124)+l.strip()[:150])
open("_spawn2.txt","w",encoding="utf-8").write(chr(10).join(out))
print("N",len(out))