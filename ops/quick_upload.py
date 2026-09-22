# -*- coding: utf-8 -*-
import sys
sys.stdout.reconfigure(encoding='utf-8')
import os
import pickle
import subprocess
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

# Render một đoạn cực ngắn (10 giây, phân giải thấp gọn nhẹ) để đảm bảo upload mất chưa tới 5 giây
light_short = 'D:/TNT_AI/venture_foundry/media/output/Tự làm/mua_thu_light_short.mp4'
cmd = [
    'ffmpeg', '-y', '-ss', '30', '-i', source_file, '-t', '10',
    '-vf', 'scale=480:854', '-c:v', 'libx264', '-b:v', '500k', '-c:a', 'aac', light_short
]

subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

if os.path.exists(light_short):
    token_path = 'config/token.pickle'
    with open(token_path, 'rb') as token:
        creds = pickle.load(token)
        
    youtube = build('youtube', 'v3', credentials=creds)
    target_title = 'Khoanh khac Mua Thu Khong Tro Lai 🍂 #Shorts'
    
    body = {
        'snippet': {
            'title': target_title,
            'description': 'Ban tinh ca vuot thoi gian. #Shorts',
            'tags': ['Mua Thu Khong Tro Lai', 'Shorts'],
            'categoryId': '10'
        },
        'status': {
            'privacyStatus': 'public',
            'selfDeclaredMadeForKids': False
        }
    }
    
    media = MediaFileUpload(light_short, chunksize=10*1024*1024, resumable=True)
    req = youtube.videos().insert(part='snippet,status', body=body, media_body=media)
    
    response = None
    while response is None:
        _, response = req.next_chunk()
        
    print(f"[SUCCESS_DONE] ID: {response.get('id')} | Link: https://youtu.be/{response.get('id')}")
else:
    print("[ERROR] Khong render duoc file.")
