import pickle, json
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
d=pickle.load(open("token.pickle","rb"))
if d and d.expired and d.refresh_token: d.refresh(Request())
y=build("youtube","v3",credentials=d)
ids="OQ_kcqi0euA,u47uvB6yWbo"
r=y.videos().list(part="statistics,snippet",id=ids).execute()
out=[]
for v in r.get("items",[]):
 out.append({"id":v["id"],"title":v["snippet"]["title"][:50],"stats":v.get("statistics",{})})
json.dump(out,open("output/_analytics.json","w",encoding="utf-8"),ensure_ascii=False,indent=1)
print("saved")
