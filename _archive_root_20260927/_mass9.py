import os, sys
os.chdir("D:/TNT_AI/venture_foundry/media")
sys.path.insert(0, "D:/TNT_AI/venture_foundry/media")
from ops import mass_producer as MP
rows = MP.run_many(limit=8, live=True)
zz = [print(r) for r in rows]
print("DONE")
