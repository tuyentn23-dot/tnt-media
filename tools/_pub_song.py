# -*- coding: utf-8 -*-
import os, sys, pickle
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ['IMAGEIO_FFMPEG_EXE'] = os.path.join(os.getcwd(), 'tools', 'ffmpeg.exe')
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

VIDEO = os.path.abspath('output/vile_lang_im_thuong_anh.mp4')
THUMB = os.path.abspath('output/vile_lang_im_thuong_anh_thumb.jpg')
TOKEN = 'config/token.pickle'

creds = pickle.load(open(TOKEN, 'rb'))
if not creds.valid and creds.refresh_token:
    creds.refresh(Request())
    pickle.dump(creds, open(TOKEN, 'wb'))
yt = build('youtube', 'v3', credentials=creds)

TITLE = 'L\u1eb7ng Im Th\u01b0\u01a1ng Anh - Nh\u1ea1c Tr\u1eef T\u00ecnh Hay Nh\u1ea5t 2026 | ViLe Vi'
DESC = ('L\u1eb7ng Im Th\u01b0\u01a1ng Anh - b\u1ea3n t\u00ecnh ca ng\u1ecdt ng\u00e0o v\u1ec1 m\u1ed9t m\u1ed1i t\u00ecnh th\u1ea7m l\u1eb7ng.\n'
 '\u0110\u0103ng k\u00fd k\u00eanh \u0111\u1ec3 nghe th\u00eam nhi\u1ec1u b\u00e0i h\u00e1t hay: @vilevi5676\n\n'
 '#LangImThuongAnh #NhacTruTinh #ViLeVi #NhacHay2026 #NhacBuon\n\n'
 '\u00a9 B\u1ea3n quy\u1ec1n thu\u1ed9c v\u1ec1 ViLe Vi. Vui l\u00f2ng kh\u00f4ng reup.')
TAGS = ['L\u1eb7ng Im Th\u01b0\u01a1ng Anh','nh\u1ea1c tr\u1eef t\u00ecnh','nh\u1ea1c hay 2026','nh\u1ea1c bu\u1ed3n','ViLe Vi','nh\u1ea1c vi\u1ec7t','t\u00ecnh ca']

body = {'snippet': {'title': TITLE, 'description': DESC, 'tags': TAGS, 'categoryId': '10'},
        'status': {'privacyStatus': 'public', 'selfDeclaredMadeForKids': False}}
media = MediaFileUpload(VIDEO, chunksize=8*1024*1024, resumable=True)
req = yt.videos().insert(part='snippet,status', body=body, media_body=media)
resp = None
while resp is None:
    status, resp = req.next_chunk()
    if status:
        print('upload', int(status.progress()*100), '%')
vid = resp.get('id')
print('VIDEO_ID', vid)
print('URL https://youtu.be/' + vid)
# set thumbnail
try:
    yt.thumbnails().set(videoId=vid, media_body=MediaFileUpload(THUMB)).execute()
    print('thumbnail set OK')
except Exception as e:
    print('thumb err', str(e)[:150])
