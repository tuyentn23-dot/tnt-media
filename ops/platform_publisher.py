import os
import logging
import datetime
import pickle

import sys as _sys
try:
    _sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    _sys.stderr.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass
# Google imports are lazy (cryptography may be unavailable on some platforms)
def _google():
    from google_auth_oauthlib.flow import InstalledAppFlow
    from googleapiclient.discovery import build
    from googleapiclient.http import MediaFileUpload
    from google.auth.transport.requests import Request
    return InstalledAppFlow, build, MediaFileUpload, Request

logging.basicConfig(
    filename='output/viral_manager.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# Nâng cấp Scope: Cho phép quản lý toàn diện kênh để vừa upload vừa lấy thống kê view/like
SCOPES = ["https://www.googleapis.com/auth/youtube"]

class MultiPlatformPublisher:
    def __init__(self, output_dir="output"):
        self.output_dir = output_dir

    def get_youtube_service(self):
        """Cấp quyền truy cập YouTube API cho các mô-đun khác (như Analytics)."""
        InstalledAppFlow, build, MediaFileUpload, Request = _google()
        credentials = None
        token_path = "token.pickle"
        client_secrets_file = "client_secret.json"

        if os.path.exists(token_path):
            with open(token_path, "rb") as token:
                credentials = pickle.load(token)

        if not credentials or not credentials.valid:
            if credentials and credentials.expired and credentials.refresh_token:
                credentials.refresh(Request())
            else:
                if not os.path.exists(client_secrets_file):
                    print(f"[Publisher Warning] Chưa tìm thấy tệp {client_secrets_file}. Bỏ qua kết nối YouTube.")
                    return None
                flow = InstalledAppFlow.from_client_secrets_file(client_secrets_file, SCOPES)
                credentials = flow.run_local_server(port=0)
            
            with open(token_path, "wb") as token:
                pickle.dump(credentials, token)

        return build("youtube", "v3", credentials=credentials)

    def publish_short(self, video_path, title="Viral Short 2026", tags=None):
        if tags is None:
            tags = ["Shorts", "Trending", "Viral", "AI"]
            
        print(f"[Platform Publisher] Đang chuẩn bị tải lên YouTube Shorts từ: {video_path}...")
        
        if not os.path.exists(video_path):
            return False
            
        try:
            youtube = self.get_youtube_service()
            if not youtube:
                simulated_id = f"MOCK_ID_{datetime.datetime.now().strftime('%H%M%S')}"
                print(f"[Publisher Mock] Trình mô phỏng tải lên. ID Mô phỏng: {simulated_id}")
                return simulated_id

            body = {
                "snippet": {
                    "title": title[:100],
                    "description": "Sản xuất tự động bởi AI Media Foundry. #Shorts #Trending",
                    "tags": tags,
                    "categoryId": "22"
                },
                "status": {
                    "privacyStatus": "public",
                    "selfDeclaredMadeForKids": False
                }
            }
            InstalledAppFlow, build, MediaFileUpload, Request = _google()

            media = MediaFileUpload(video_path, chunksize=-1, resumable=True)
            request = youtube.videos().insert(part="snippet,status", body=body, media_body=media)

            response = None
            while response is None:
                status, response = request.next_chunk()
                if status:
                    print(f"[Upload Progress] Đã tải lên được {int(status.progress() * 100)}%")

            video_id = response.get('id')
            publish_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            print(f"🚀 [SUCCESS] Video đã tải lên YouTube Shorts thành công! ID: {video_id} lúc {publish_time}")
            return video_id
            
        except Exception as e:
            err_msg = f"[Publisher Error]: {str(e)}"
            print(err_msg)
            logging.error(err_msg)
            return False

PUBLISHER = None

def unified_publish(video_path, title=None, tags=None):
    global PUBLISHER
    if PUBLISHER is None:
        PUBLISHER = MultiPlatformPublisher()
    return PUBLISHER.publish_short(video_path, title or "Viral Short 2026", tags)
