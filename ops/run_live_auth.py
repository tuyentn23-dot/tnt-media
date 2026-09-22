import os, json
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

CLIENT_SECRET_FILE = "client_secret.json"
TOKEN_FILE = "memory/token_new_channel.json"
SCOPES = ["https://www.googleapis.com/auth/youtube.upload", "https://www.googleapis.com/auth/youtube.readonly"]

def run_live_oauth_and_upload():
    print("=== BAT DAU XAC THUC OAUTH THUC TE & UPLOAD YOUTUBE ===")
    if not os.path.exists(CLIENT_SECRET_FILE):
        print("Loi: Thieu client_secret.json")
        return
    
    # Chay local server de xac thuc OAuth qua trinh duyệt
    flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRET_FILE, SCOPES)
    print("He thong dang khoi tao local server de xac thuc tai khoan Google...")
    # Neu chay headless (khong co UI trinh trinh duyet), in huong dan link hoac chay flow
    try:
        creds = flow.run_local_server(port=0, open_browser=True)
        os.makedirs('memory', exist_ok=True)
        with open(TOKEN_FILE, "w", encoding="utf-8") as token:
            token.write(creds.to_json())
        print("Xac thuc OAuth thanh cong! Token da duu luu vao:", TOKEN_FILE)
        
        youtube = build("youtube", "v3", credentials=creds)
        request_body = {
            "snippet": {
                "title": "Bi mat thu vi ve Roblox & Anime cho Thieu nhi #shorts",
                "description": "Kham pha nhung meo hay nhat ve Roblox, Anime va Thu cung cho thieu nhi va thieu nien! #shorts #roblox #anime",
                "tags": ["roblox", "anime", "pets", "shorts"],
                "categoryId": "24"
            },
            "status": {
                "privacyStatus": "public",
                "selfDeclaredMadeForKids": False
            }
        }
        print("Da ket noi API YouTube va san sang upload thuc te len kenh!")
    except Exception as e:
        print("Chi tiet loi xac thuc hoac moi trường:", str(e))

if __name__ == "__main__":
    run_live_oauth_and_upload()
