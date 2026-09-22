# -*- coding: utf-8 -*-
import os
import sys
sys.stdout.reconfigure(encoding='utf-8')
import pickle
import shutil
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

print("[PIPELINE] Bat dau quy trinh tu dong dang YouTube Short...")

source_file = 'D:/TNT_AI/venture_foundry/media/output/Tự làm/Mùa Thu Không Trở Lại.mp4'
if not os.path.exists(source_file):
    source_file = 'D:/TNT_AI/venture_foundry/media/output/Tu lam/Mua Thu Khong Tro Lai.mp4'

# Sử dụng trực tiếp file chuẩn làm Shorts hoặc tạo bản sao với tên không dấu để upload an toàn tuyệt đối
short_output = 'D:/TNT_AI/venture_foundry/media/output/Tự làm/mua_thu_short.mp4'
if not os.path.exists(short_output):
    shutil.copyfile(source_file, short_output)

if os.path.exists(short_output):
    print(f"[SUCCESS] San sang file Short: {short_output}")
    
    token_path = 'config/token.pickle'
    if os.path.exists(token_path):
        with open(token_path, 'rb') as token:
            creds = pickle.load(token)
            
        youtube = build('youtube', 'v3', credentials=creds)
        body = {
            'snippet': {
                'title': 'Khoanh khac lang dong cung Mua Thu Khong Tro Lai #Shorts #NhacTruTinh',
                'description': 'Ban tinh ca vuot thoi gian goi nho bao ky niem hoai niem mua thu. #MuaThuKhongTroLai #NhacXua #Shorts',
                'tags': ['Mua Thu Khong Tro Lai', 'nhac tru tinh', 'nhac xua', 'Shorts'],
                'categoryId': '10'
            },
            'status': {
                'privacyStatus': 'public',
                'selfDeclaredMadeForKids': False
            }
        }
        
        media = MediaFileUpload(short_output, chunksize=5*1024*1024, resumable=True)
        req = youtube.videos().insert(part='snippet,status', body=body, media_body=media)
        
        resp = None
        while resp is None:
            status, resp = req.next_chunk()
            if status:
                print(f"[UPLOAD] Tien trinh Shorts: {int(status.progress() * 100)}%")
                
        print(f"[SUCCESS] Dang YouTube Short thanh công! Video ID: {resp.get('id')}")
        print(f"[LINK] https://youtu.be/{resp.get('id')}")
else:
    print("[ERROR] Khong tim thay file.")
