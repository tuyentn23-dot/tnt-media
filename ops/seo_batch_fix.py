import os,sys,json,pickle
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0,ROOT)
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
d=pickle.load(open(os.path.join(ROOT,"token.pickle"),"rb"))
if d and d.expired and d.refresh_token: d.refresh(Request())
yt=build("youtube","v3",credentials=d)
pub=json.load(open(os.path.join(ROOT,"memory","published.json"),encoding="utf-8"))
ids=[v["youtube_id"] for v in pub["videos"] if v.get("youtube_id")][-50:]
SH=chr(35)+"shorts"
def fix(vid):
    try:
        r=yt.videos().list(part="snippet,status",id=vid).execute()
        if not r["items"]: return "gone"
        sn=dict(r["items"][0]["snippet"]); st=dict(r["items"][0]["status"])
        t=sn.get("title","")
        if "shorts" not in t.lower(): sn["title"]=t+" #shorts"
        if len(sn.get("description",""))<80: sn["description"]=t+chr(10)+chr(10)+"#shorts #viral #facts"
        if not sn.get("tags"): sn["tags"]=["shorts","viral","facts"]
        body={"id":vid,"snippet":sn,"status":{"privacyStatus":st.get("privacyStatus","public"),"selfDeclaredMadeForKids":False}}
        yt.videos().update(part="snippet,status",body=body).execute()
        return "fixed"
    except Exception as e: return str(e)[:60]
res={}
for vid in ids: res[vid]=fix(vid)
json.dump(res,open(os.path.join(ROOT,"memory/seo_batch_result.json"),"w"))
print("fixed:",len([x for x in res.values() if x=="fixed"]))
