# -*- coding: utf-8 -*-
import sys
sys.stdout.reconfigure(encoding='utf-8')
import os
import pickle
import shutil
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

source_files = [
    'D:/TNT_AI/venture_foundry/media/output/Tự làm/Mùa Thu Không Trở Lại.mp4',
    'D:/TNT_AI/venture_foundry/media/output/Tu lam/Mua Thu Khong Tro Lai.mp4'
]

source_file = None
for path in source_files:
    if os.path.exists(path):
        source_file = path
        break

if not source_file:
    print("[ERROR] Khong tim thay file goc.")
    sys.exit(1)

fresh_short_output = 'D:/TNT_AI/venture_foundry/media/output/Tự làm/mua_thu_short_v3_final.mp4'
shutil.copyfile(source_file, fresh_short_output)

token_path = 'config/token.pickle'
with open(token_path, 'rb') as token:
    creds = pickle.load(token)

youtube = build('youtube', 'v3', credentials=creds)
target_title = 'Khoanh khac lang dong Mua Thu Khong Tro Lai - Ban Chuan 🍂 #Shorts'

# Kiem tra chong trung lap tuyet doi
search_req = youtube.search().list(part='snippet', forMine=True, type='video', maxResults=5)
search_res = search_req.execute()

exists = False
for item in search_res.get('items', []):
    if item['snippet']['title'] == target_title:
        exists = True
        break

if exists:
    print("[ABORT] Video da ton tai tren kenh. Huy dang.")
else:
    print("[UPLOAD] Dang tai len 1 video Short duy nhat...")
    body = {
        'snippet': {
            'title': target_title,
            'description': 'Ban tinh ca vuot thoi gian goi nho bao ky niem hoai niem mua thu. #MuaThuKhongTroLai #NhacXua #Shorts',
            'tags': ['Mua Thu Khong Tro Lai', 'nhac tru tinh', 'nhac xua', 'Shorts'],
            'categoryId': '10'
        },
        'status': {
            'privacyStatus': 'public',
            'selfDeclaredMadeForKids': False
        }
    }
    
    media = MediaFileUpload(fresh_short_output, chunksize=5*1024*1024, resumable=True)
    req = youtube.videos().insert(part='snippet,status', body=body, media_body=media)
    
    response = None
    while response is None:
        status, response = req.next_chunk()
        if status:
            print(f"[UPLOAD PROGRESS] {int(status.progress() * 100)}%")
            
    print(f"[SUCCESS] Dang YouTube Short thanh cong! ID: {response.get('id')}")
    print(f"- Link: https://youtu.be/{response.get('id')}")
