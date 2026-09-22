import pickle
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
d=pickle.load(open("token.pickle","rb"))
if d and d.expired and d.refresh_token: d.refresh(Request())
y=build("youtube","v3",credentials=d)
ch=y.channels().list(part="brandingSettings",mine=True).execute()
items=ch.get("items",[])
if items:
 b=items[0].get("brandingSettings",{})
 ch2=b.get("channel",{})
 ch2["featuredVideoId"]="OQ_kcqi0euA"
 y.channels().update(part="brandingSettings",body={"id":items[0]["id"],"brandingSettings":b}).execute()
 print("FEATURED SET")
else: print("no")
