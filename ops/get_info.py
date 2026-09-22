import pickle, json
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
d=pickle.load(open("token.pickle","rb"))
if d and d.expired and d.refresh_token: d.refresh(Request())
y=build("youtube","v3",credentials=d)
r=y.videos().list(part="snippet",id="OQ_kcqi0euA").execute()
sn=r["items"][0]["snippet"]
out={"title":sn["title"],"desc":sn.get("description",""),"tags":sn.get("tags",[]),"thumbs":list(sn.get("thumbnails",{}).keys())}
json.dump(out,open("output/_vinfo.json","w",encoding="utf-8"),ensure_ascii=False,indent=1)
print("saved")
