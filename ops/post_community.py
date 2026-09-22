import pickle
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
d=pickle.load(open("token.pickle","rb"))
if d and d.expired and d.refresh_token: d.refresh(Request())
y=build("youtube","v3",credentials=d)
msg="test post"
body={"snippet":{"type":"textOriginal","textOriginal":msg}}
try:
 r=y.activities().insert(part="snippet",body=body).execute()
 print("POSTED")
except Exception as e: print("ERR",str(e)[:150])
