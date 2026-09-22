import sys
sys.stdout.reconfigure(encoding='utf-8')
import os
import traceback
import google.auth
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from google_auth_oauthlib.flow import InstalledAppFlow

try:
    video_path = 'D:/TNT_AI/venture_foundry/media/output/Tự làm/Mùa Thu Không Trở Lại.mp4'
    if not os.path.exists(video_path):
        video_path = 'D:/TNT_AI/venture_foundry/media/output/Tu lam/Mua Thu Khong Tro Lai.mp4'
    
    print('[INFO] Duong dan video: ' + video_path)
    if not os.path.exists(video_path):
        print('[ERROR] Khong tim thay file video!')
        exit(1)
        
    # Đọc mô tả từ file ngoài để tránh mọi lỗi cú pháp xuống dòng
    desc_path = os.path.join('ops', 'desc.txt')
    if os.path.exists(desc_path):
        with open(desc_path, 'r', encoding='utf-8') as df:
            desc = df.read()
    else:
        desc = 'Thuong thuc ca khuc Mua Thu Khong Tro Lai.'
        
    import pickle
    SCOPES = ['https://www.googleapis.com/auth/youtube.upload', 'https://www.googleapis.com/auth/youtube.readonly']
    creds = None
    token_path = 'config/token.pickle'
    if os.path.exists(token_path):
        with open(token_path, 'rb') as token:
            creds = pickle.load(token)
    if not creds or not creds.valid:
        try:
            if creds and creds.expired and creds.refresh_token:
                from google.auth.transport.requests import Request
                creds.refresh(Request())
            else:
                raise Exception("Invalid")
        except Exception:
            if os.path.exists(token_path):
                os.remove(token_path)
            flow = InstalledAppFlow.from_client_secrets_file('D:/TNT_AI/venture_foundry/media/config/client_secrets.json', SCOPES)
            creds = flow.run_local_server(port=0)
        with open(token_path, 'wb') as token:
            pickle.dump(creds, token)
    youtube = build('youtube', 'v3', credentials=creds)
    
    body = {
        'snippet': {
            'title': '[Official Audio] Mua Thu Khong Tro Lai - Tuyen Tap Nhac Tru Tinh Mua Thu Bat Hu',
            'description': desc,
            'tags': ['Mua Thu Khong Tro Lai', 'nhac tru tinh mua thu', 'album nhac mua thu'],
            'categoryId': '10'
        },
        'status': {
            'privacyStatus': 'private',
            'selfDeclaredMadeForKids': False
        }
    }
    
    media = MediaFileUpload(video_path, chunksize=-1, resumable=True)
    req = youtube.videos().insert(part='snippet,status', body=body, media_body=media)
    
    resp = None
    while resp is None:
        status, resp = req.next_chunk()
        if status:
            print('[UPLOAD] Tien trinh: ' + str(int(status.progress() * 100)) + '%')
            
    print('[SUCCESS] Upload thanh cong! Video ID: ' + str(resp.get('id')))
    print('[LINK] https://youtu.be/' + str(resp.get('id')))
except Exception as e:
    traceback.print_exc()
