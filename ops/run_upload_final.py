import os
import traceback
import google.auth
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from google_auth_oauthlib.flow import InstalledAppFlow

try:
    video_path = os.path.abspath("output/Tu lam/Mua Thu Khong Tro Lai.mp4")
    if not os.path.exists(video_path):
        video_path = "D:/TNT_AI/venture_foundry/media/output/Tu lam/Mua Thu Khong Tro Lai.mp4"
    
    print(f"[INFO] Duong dan video: {video_path}")
    if not os.path.exists(video_path):
        print("[ERROR] Khong tim thay file video!")
        exit(1)
        
    SCOPES = ["https://www.googleapis.com/auth/youtube.upload", "https://www.googleapis.com/auth/youtube.readonly"]
    flow = InstalledAppFlow.from_client_secrets_file("client_secret.json", SCOPES)
    creds = flow.run_local_server(port=0)
    youtube = build("youtube", "v3", credentials=creds)
    
    desc = "Thuong thuc ca khuc Mua Thu Khong Tro Lai - ban tinh ca vuot thoi gian.

Album Mua Thu Tru Tinh
#MuaThuKhongTroLai #NhacTruTinh"
    
    body = {
        "snippet": {
            "title": "[Official Audio] Mua Thu Khong Tro Lai - Tuyen Tap Nhac Tru Tinh Mua Thu Bat Hu",
            "description": desc,
            "tags": ["Mua Thu Khong Tro Lai", "nhac tru tinh mua thu", "album nhac mua thu"],
            "categoryId": "10"
        },
        "status": {
            "privacyStatus": "private",
            "selfDeclaredMadeForKids": False
        }
    }
    
    media = MediaFileUpload(video_path, chunksize=-1, resumable=True)
    req = youtube.videos().insert(part="snippet,status", body=body, media_body=media)
    
    resp = None
    while resp is None:
        status, resp = req.next_chunk()
        if status:
            print(f"[UPLOAD] Tien trinh: {int(status.progress() * 100)}%")
            
    print(f"[SUCCESS] Upload thanh cong! Video ID: {resp.get('id')}")
    print(f"[LINK] https://youtu.be/{resp.get('id')}")
except Exception as e:
    traceback.print_exc()
