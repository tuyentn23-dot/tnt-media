import os, shutil
src = 'ops/output/CHECK'
dst = 'output/CHECK'
os.makedirs(dst, exist_ok=True)
moved = 0
for fn in os.listdir(src):
	if fn.startswith('anime_final_'):
		s = os.path.join(src, fn)
		d = os.path.join(dst, fn)
		shutil.move(s, d)
		moved += 1
print('moved', moved)
print('dst count:', len([f for f in os.listdir(dst) if f.startswith('anime_final_')]))