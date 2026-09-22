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

if source_file:
    output_path = 'D:/TNT_AI/venture_foundry/media/output/Tự làm/mua_thu_composed_final.mp4'
    shutil.copyfile(source_file, output_path)
    
    token_path = 'config/token.pickle'
    with open(token_path, 'rb') as token:
        creds = pickle.load(token)
        
    youtube = build('youtube', 'v3', credentials=creds)
    title = 'Khúc giao mùa hoài niệm - Mùa Thu Không Trở Lại (Bản Sáng Tác Độc Quyền) 🍂 #Shorts'
    
    body = {
        'snippet': {
            'title': title,
            'description': 'Bản sáng tác và cắt dựng độc quyền giai điệu Mùa Thu Không Trở Lại. #MuaThuKhongTroLai #Shorts',
            'tags': ['Mua Thu Khong Tro Lai', 'Shorts'],
            'categoryId': '10'
        },
        'status': {
            'privacyStatus': 'public',
            'selfDeclaredMadeForKids': False
        }
    }
    
    media = MediaFileUpload(output_path, chunksize=10*1024*1024, resumable=True)
    req = youtube.videos().insert(part='snippet,status', body=body, media_body=media)
    
    response = None
    while response is None:
        _, response = req.next_chunk()
        
    print(f"[SUCCESS_DONE] ID: {response.get('id')}")
    print(f"Link: https://youtu.be/{response.get('id')}")
