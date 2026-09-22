
import os
import pickle
import time
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

try:
    token_path = 'config/token.pickle'
    with open(token_path, 'rb') as token:
        creds = pickle.load(token)

    video_path = 'D:/TNT_AI/venture_foundry/media/output/Tự làm/Mùa Thu Không Trở Lại.mp4'
    youtube = build('youtube', 'v3', credentials=creds)
    body = {
        'snippet': {
            'title': '[Official Audio] Mua Thu Khong Tro Lai - Tuyen Tap Nhac Tru Tinh Mua Thu Bat Hu',
            'description': 'Thuong thuc ca khuc Mua Thu Khong Tro Lai.',
            'tags': ['Mua Thu Khong Tro Lai', 'nhac tru tinh mua thu', 'album nhac mua thu'],
            'categoryId': '10'
        },
        'status': {
            'privacyStatus': 'private',
            'selfDeclaredMadeForKids': False
        }
    }

    media = MediaFileUpload(video_path, chunksize=32*1024*1024, resumable=True)
    req = youtube.videos().insert(part='snippet,status', body=body, media_body=media)

    resp = None
    while resp is None:
        status, resp = req.next_chunk()
        if status:
            with open('ops/upload_progress.log', 'w', encoding='utf-8') as log:
                log.write(f"{int(status.progress() * 100)}%")

    video_id = resp.get('id')
    with open('ops/upload_result.txt', 'w', encoding='utf-8') as f:
        f.write(video_id)
    with open('ops/upload_progress.log', 'w', encoding='utf-8') as log:
        log.write("COMPLETED: " + video_id)
except Exception as e:
    with open('ops/upload_progress.log', 'w', encoding='utf-8') as log:
        log.write("ERROR: " + str(e))
