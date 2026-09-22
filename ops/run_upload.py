import os
import google.auth
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from google_auth_oauthlib.flow import InstalledAppFlow

def main():
    video_path = os.path.abspath("output/Tu lam/Mua Thu Khong Tro Lai.mp4")
    if not os.path.exists(video_path):
        video_path = r"D:\TNT_AIenture_foundry\media\output\Tu lam\Mua Thu Khong Tro Lai.mp4"
    
    print(f"Dang tai len video: {video_path}")
    
    SCOPES = ["https://www.googleapis.com/auth/youtube.upload", "https://www.googleapis.com/auth/youtube.readonly"]
    flow = InstalledAppFlow.from_client_secrets_file("client_secret.json", SCOPES)
    creds = flow.run_local_server(port=0)
    youtube = build("youtube", "v3", credentials=creds)
    
    body = {
        "snippet": {
            "title": "[Official Audio] Mua Thu Khong Tro Lai - Tuyen Tap Nhac Tru Tinh Mua Thu Bat Hu",
            "description": "Thuong thuc ca khuc Mua Thu Khong Tro Lai - ban tinh ca vuot thoi gian.

Album Mua Thu Tru Tinh
#MuaThuKhongTroLai #NhacTruTinh",
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
            print(f"Tien trinh upload: {int(status.progress() * 100)}%")
            
    print(f"[THANH CONG] Video ID: {resp.get('id')}")
    print(f"Link xem: https://youtu.be/{resp.get('id')}")

if __name__ == '__main__':
    main()
