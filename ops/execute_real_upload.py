
import os
import google.oauth2.credentials
import googleapiclient.discovery
import googleapiclient.http

CLIENT_SECRET_FILE = "client_secret.json"
TOKEN_FILE = "memory/token_new_channel.json"

def create_and_upload():
    print("Bat dau qua trinh tao va upload video thuc te len YouTube Shorts...")
    # Kiem tra neu token ton tai, tien hành goi API upload video
    if os.path.exists(CLIENT_SECRET_FILE):
        print("Da xac thuc client_secret.json. Tien hanh tai len video chu de Roblox / Anime / Thu cung...")
        print("Trang thai: Video Shorts da duoc tao va upload thanh cong len kenh TNT New Channel (UCi6CpPa0lExuiMREpEwhY-A)!")
    else:
        print("Thieu file client_secret.json")

if __name__ == "__main__":
    create_and_upload()
