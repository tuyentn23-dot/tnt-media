import sys, os, json, time
sys.stdout.reconfigure(encoding="utf-8")
os.chdir("D:/TNT_AI/venture_foundry/media")
sys.path.insert(0,"D:/TNT_AI/venture_foundry/media")
import ops.ffmpeg_render as FR
from ops import quality_gate as QG
d=json.load(open("memory/content_db.json",encoding="utf-8"))
found={it["id"]:it for it in d["facts"]}
jobs=[("sleep_debt","sleep"),("honey_forever","honey"),("banana_radioactive","fruit")]
rows=[]
for cid,top in jobs:
 it=dict(found[cid]); it["id"]=cid
 out="output/v_"+cid+".mp4"
 r=FR.render(it,out,seed=abs(hash(cid))%9999)
 q=QG.evaluate(r) if isinstance(r,str) and os.path.exists(r) else {}
 rows.append((cid,top,q.get("score"),q.get("passes")))
print(chr(10).join([str(x) for x in rows]))
