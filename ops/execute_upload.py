
import os
import pickle
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

token_path = 'config/token.pickle'
with open(token_path, 'rb') as token:
    creds = pickle.load(token)

video_path = 'D:/TNT_AI/venture_foundry/media/output/Tự làm/Mùa Thu Không Trở Lại.mp4'
if not os.path.exists(video_path):
    video_path = 'D:/TNT_AI/venture_foundry/media/output/Tu lam/Mua Thu Khong Tro Lai.mp4'

file_size = os.path.getsize(video_path)
print(f"File size: {file_size / (1024*1024):.2f} MB")

youtube = build('youtube', 'v3', credentials=creds)
body = {
    'snippet': {
        'title': '[Official Audio] Mua Thu Khong Tro Lai - Tuyen Tap Nhac Tru Tinh Mua Thu Bat Hu',
        'description': 'Thuong thuc ca khuc Mua Thu Khong Tro Lai.',
        'tags': ['Mua Thu Khong TroLai', 'nhac tru tinh mua thu', 'album nhac mua thu'],
        'categoryId': '10'
    },
    'status': {
        'privacyStatus': 'private',
        'selfDeclaredMadeForKids': False
    }
}

media = MediaFileUpload(video_path, chunksize=1024*1024*10, resumable=True)
req = youtube.videos().insert(part='snippet,status', body=body, media_body=media)

resp = None
while resp is None:
    status, resp = req.next_chunk()
    if status:
        print(f"Uploaded {int(status.progress() * 100)}%")

print(f"SUCCESS_ID: {resp.get('id')}")
