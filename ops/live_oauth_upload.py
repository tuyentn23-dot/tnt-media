import os
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

SCOPES = ["https://www.googleapis.com/auth/youtube.upload", "https://www.googleapis.com/auth/youtube.readonly"]
CLIENT_SECRET_FILE = "client_secret.json"
TOKEN_FILE = "memory/token_new_channel.json"

def authenticate():
    print("=== BAT DAU XAC THUC OAUTH THUC TE CHO YOUTUBE API ===")
    if not os.path.exists(CLIENT_SECRET_FILE):
        print("Loi: Khong tim thay tep client_secret.json!")
        return
    
    flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRET_FILE, SCOPES)
    creds = flow.run_local_server(port=0)
    
    os.makedirs('memory', exist_ok=True)
    with open(TOKEN_FILE, "w", encoding="utf-8") as token:
        token.write(creds.to_json())
    print(f"Da luu token that thanh cong vao: {TOKEN_FILE}")
    
    youtube = build("youtube", "v3", credentials=creds)
    channels_response = youtube.channels().list(mine=True, part="snippet,statistics").execute()
    if channels_response.get("items"):
        channel_info = channels_response["items"][0]
        print(f"Da ket noi thanh cong voi kenh: {channel_info['snippet']['title']} (ID: {channel_info['id']})")
    else:
        print("Khong tim thay thong tin kenh lien ket.")

if __name__ == "__main__":
    authenticate()
