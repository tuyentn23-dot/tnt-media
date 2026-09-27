import os, sys
os.chdir("D:/TNT_AI/venture_foundry/media")
sys.path.insert(0, "D:/TNT_AI/venture_foundry/media")
from ops import mass_producer as MP
print("ROUND 0")
rows = MP.run_many(limit=5, live=True)
zz = [print(r) for r in rows]
print("ROUND 1")
rows = MP.run_many(limit=5, live=True)
zz = [print(r) for r in rows]
