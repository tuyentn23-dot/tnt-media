# perf_tracker.py - pull real stats, log to memory, show trends
import os,sys,json,pickle
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)
from google.auth.transport.requests import Request
from googleapiclient.discovery import build

def yt():
    d = pickle.load(open(os.path.join(ROOT,"token.pickle"),"rb"))
    if d and d.expired and d.refresh_token: d.refresh(Request())
    return build("youtube","v3",credentials=d)

def track():
    pub = json.load(open(os.path.join(ROOT,"memory","published.json"),encoding="utf-8"))
    ids = [v["youtube_id"] for v in pub["videos"] if v.get("youtube_id")]
    ids = ids[-50:]
    y = yt()
    out = []
    for i in range(0,len(ids),50):
        r = y.videos().list(part="statistics,status",id=",".join(ids[i:i+50])).execute()
        for v in r.get("items",[]):
            s = v.get("statistics",{})
            out.append({"id":v["id"],"views":int(s.get("viewCount",0)),"likes":int(s.get("likeCount",0)),"comments":int(s.get("commentCount",0)),"status":v["status"]["privacyStatus"]})
    json.dump(out,open(os.path.join(ROOT,"memory","performance.json"),"w"),indent=2)
    return out

if __name__ == "__main__":
    d = track()
    print("tracked", len(d))
