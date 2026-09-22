# make_video.py - build high-quality retention video from content_db
import os, sys, json
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0,ROOT)
DB=os.path.join(ROOT,"memory","content_db.json")
def pick(kind,idx):
 d=json.load(open(DB,encoding="utf-8"))
 return d[kind][idx]
if __name__=="__main__":
 kind=sys.argv[1] if len(sys.argv)>1 else "facts"
 idx=int(sys.argv[2]) if len(sys.argv)>2 else 0
 item=pick(kind,idx)
 from ops.content_video5 import build
 out=os.path.join(ROOT,"output","v5_"+item["id"]+".mp4")
 print("building",item["id"])
 build(item,out)
 print("DONE",out)
