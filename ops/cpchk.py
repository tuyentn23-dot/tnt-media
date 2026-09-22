import os,sys,json
sys.path.insert(0,os.getcwd())
from ops import content_planner as cp
for t in ['anime','roblox']:
    h, lines, hint = cp.for_topic(t)
    print(t, json.dumps(h, ensure_ascii=True))
    print(t, json.dumps(lines, ensure_ascii=True))
