import os, shutil
keep = ["STATE.md", "REFERENCE.md"]
dst = "_archive/root_docs"
os.makedirs(dst, exist_ok=True)
moved = 0
for f in os.listdir(chr(46)):
	if f.endswith(chr(46) + chr(109) + chr(100)) and f not in keep:
		shutil.move(f, os.path.join(dst, f))
		moved += 1
print("moved ", moved)
print("root md: ", [f for f in os.listdir(chr(46)) if f.endswith(chr(46) + chr(109) + chr(100))])