# ops/publish_one.py - Real YouTube Production Uploader
import os
import json
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials

SCOPES = ['https://www.googleapis.com/auth/youtube']
API_SERVICE_NAME = 'youtube'
API_VERSION = 'v3'

def get_authenticated_service():
    credentials = None
    token_file = 'memory/token.json'
    
    client_secrets_file = 'client_secrets.json'
    if not os.path.exists(client_secrets_file):
        if os.path.exists('config/client_secrets.json'):
            client_secrets_file = 'config/client_secrets.json'
    
    if os.path.exists(token_file):
        try:
            credentials = Credentials.from_authorized_user_file(token_file, SCOPES)
        except Exception:
            credentials = None
    
    if not credentials or not credentials.valid:
        if credentials and credentials.expired and credentials.refresh_token:
            try:
                credentials.refresh(Request())
            except Exception:
                credentials = None
                
        if not credentials:
            if not os.path.exists(client_secrets_file):
                raise FileNotFoundError("Khong tim thay client_secrets.json.")
            
            flow = InstalledAppFlow.from_client_secrets_file(client_secrets_file, SCOPES)
            print("\n[YOUTUBE AUTH] Vui long xac thuc tai khoan bang duong dan ben duoi:")
            credentials = flow.run_console()
        
        os.makedirs('memory', exist_ok=True)
        with open(token_file, 'w', encoding='utf-8') as token:
            token.write(credentials.to_json())
            
    return build(API_SERVICE_NAME, API_VERSION, credentials=credentials)

def upload(video_path, title, desc, tags):
    if not os.path.exists(video_path):
        raise FileNotFoundError(f"Khong tim thay file video: {video_path}")
        
    print("[REAL UPLOAD] Ket noi YouTube API...")
    youtube = get_authenticated_service()
    
    body = {
        "snippet": {
            "title": title[:100],
            "description": desc,
            "tags": tags,
            "categoryId": "22"
        },
        "status": {
            "privacyStatus": "public",
            "selfDeclaredMadeForKids": False,
            "containsSyntheticMedia": True
        }
    }
    
    media = MediaFileUpload(video_path, chunksize=-1, resumable=True, mimetype="video/mp4")
    request = youtube.videos().insert(
        part="snippet,status",
        body=body,
        media_body=media
    )
    
    response = None
    while response is None:
        status, response = request.next_chunk()
        if status:
            print(f"[UPLOAD] Da tai len {int(status.progress() * 100)}%")
            
    video_id = response.get('id')
    print(f"[REAL UPLOAD THANH CONG] Video ID: {video_id}")
    return video_id

def record(meta):
    try:
        os.makedirs('memory', exist_ok=True)
        path = 'memory/published.json'
        data = []
        if os.path.exists(path):
            try:
                with open(path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
            except Exception:
                data = []
        if not isinstance(data, list):
            data = []
        data.append(meta)
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        print("[RECORD] Da ghi nhan lich su thanh cong.")
    except Exception as e:
        print(f"[RECORD ERROR] {e}")
