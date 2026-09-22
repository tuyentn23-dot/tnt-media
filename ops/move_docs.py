import os, shutil
src_dir = "docs"
dst_dir = "_archive/docs_old"
os.makedirs(dst_dir, exist_ok=True)
moved = 0
for f in os.listdir(src_dir):
	if f.endswith(".md"):
		s = os.path.join(src_dir, f)
		d = os.path.join(dst_dir, f)
		shutil.move(s, d)
		moved += 1
print("moved ", moved)
print("docs now: ", os.listdir("docs"))
print("archive: ", os.listdir(dst_dir))