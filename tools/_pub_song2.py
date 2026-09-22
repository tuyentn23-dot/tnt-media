# -*- coding: utf-8 -*-
import os, sys, pickle
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
VIDEO=os.path.abspath('output/vile_youaremyonlyone.mp4')
THUMB=os.path.abspath('output/vile_youaremyonlyone_thumb.jpg')
TOKEN='config/token.pickle'
creds=pickle.load(open(TOKEN,'rb'))
if not creds.valid and creds.refresh_token:
    creds.refresh(Request()); pickle.dump(creds, open(TOKEN,'wb'))
yt=build('youtube','v3',credentials=creds)
TITLE='You Are My Only One - Nh\u1ea1c Tr\u1eef T\u00ecnh Ng\u1ecdt Ng\u00e0o | ViLe Vi'
DESC=('You Are My Only One - b\u1ea3n t\u00ecnh ca ng\u1ecdt ng\u00e0o d\u00e0nh cho ng\u01b0\u1eddi b\u1ea1n y\u00eau.\n'
 '\u0110\u0103ng k\u00fd k\u00eanh: @vilevi5676\n\n'
 '#YouAreMyOnlyOne #NhacTruTinh #ViLeVi #NhacHay2026 #NhacBuon\n\n'
 '\u00a9 B\u1ea3n quy\u1ec1n thu\u1ed9c v\u1ec1 ViLe Vi.')
TAGS=['You Are My Only One','nh\u1ea1c tr\u1eef t\u00ecnh','nh\u1ea1c hay 2026','nh\u1ea1c bu\u1ed3n','ViLe Vi','t\u00ecnh ca','nh\u1ea1c vi\u1ec7t']
body={'snippet':{'title':TITLE,'description':DESC,'tags':TAGS,'categoryId':'10'},'status':{'privacyStatus':'public','selfDeclaredMadeForKids':False}}
media=MediaFileUpload(VIDEO,chunksize=8*1024*1024,resumable=True)
req=yt.videos().insert(part='snippet,status',body=body,media_body=media)
resp=None
while resp is None:
    st,resp=req.next_chunk()
    if st: print('upload', int(st.progress()*100),'%')
vid=resp.get('id')
print('VIDEO_ID',vid)
print('URL https://youtu.be/'+vid)
try:
    yt.thumbnails().set(videoId=vid,media_body=MediaFileUpload(THUMB)).execute()
    print('thumb OK')
except Exception as e:
    print('thumb err',str(e)[:120])
