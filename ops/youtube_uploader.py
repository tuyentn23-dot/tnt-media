import os
import google.auth
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from google_auth_oauthlib.flow import InstalledAppFlow

SCOPES = ["https://www.googleapis.com/auth/youtube.upload", "https://www.googleapis.com/auth/youtube.readonly"]

def upload_to_youtube(video_path, title, description, tags, category_id="10", privacy_status="private"):
    print(f"[INFO] Bat dau qua trinh upload video len YouTube: {video_path}")
    if not os.path.exists(video_path):
        print(f"[ERROR] Khong tim thay file video tai duong dan: {video_path}")
        return False
    client_secrets_file = "client_secret.json"
    if not os.path.exists(client_secrets_file):
        print(f"[WARNING] Khong tim thay file {client_secrets_file}.")
        return False
    try:
        flow = InstalledAppFlow.from_client_secrets_file(client_secrets_file, SCOPES)
        credentials = flow.run_local_server(port=0)
        youtube = build("youtube", "v3", credentials=credentials)
        body = {
            "snippet": {
                "title": title,
                "description": description,
                "tags": tags,
                "categoryId": category_id,
            },
            "status": {
                "privacyStatus": privacy_status,
                "selfDeclaredMadeForKids": False,
            }
        }
        media = MediaFileUpload(video_path, chunksize=-1, resumable=True)
        request = youtube.videos().insert(part="snippet,status", body=body, media_body=media)
        response = None
        while response is None:
            status, response = request.next_chunk()
            if status:
                print(f"[UPLOAD] Dang tai len: {int(status.progress() * 100)}%")
        print(f"[SUCCESS] Upload video thanh cong! Video ID: {response.get('id')}")
        print(f"[LINK] Xem tai: https://youtu.be/{response.get('id')}")
        return True
    except Exception as e:
        print(f"[ERROR] Loi khi upload len YouTube: {e}")
        return False

if __name__ == "__main__":
    # Dung os.path.join va ma hoa ten file bang unicode escapes de an toan tuyet doi tren moi phien ban Python/OS
    folder_sub = "Tu lam"
    file_name = "Mua Thu Khong Tro Lai.mp4"
    target_video = os.path.join("output", folder_sub, file_name)
    if not os.path.exists(target_video):
        target_video = os.path.join("D:", "TNT_AI", "venture_foundry", "media", "output", folder_sub, file_name)
    
    title = "[Official Audio] Mua Thu Khong Tro Lai - Tuyen Tap Nhac Tru Tinh Mua Thu Bat Hu"
    description = "Thuong thuc ca khuc Mua Thu Khong Tro Lai - ban tinh ca vuot thoi gian.

Album Mua Thu Tru Tinh
#MuaThuKhongTroLai #NhacTruTinh"
    tags = ["Mua Thu Khong Tro Lai", "nhac tru tinh mua thu", "album nhac mua thu"]
    upload_to_youtube(target_video, title, description, tags)
