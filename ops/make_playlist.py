import pickle, json
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
d=pickle.load(open("token.pickle","rb"))
if d and d.expired and d.refresh_token: d.refresh(Request())
y=build("youtube","v3",credentials=d)
cfg=json.load(open("output/_pl_cfg.json",encoding="utf-8"))
body={"snippet":{"title":cfg["title"],"description":cfg.get("desc","")},"status":{"privacyStatus":"public"}}
pl=y.playlists().insert(part="snippet,status",body=body).execute()
pid=pl["id"]
print("PLAYLIST "+pid)
json.dump({"id":pid},open("output/_pl_id.json","w"),indent=1)
