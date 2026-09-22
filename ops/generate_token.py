
import os
from google_auth_oauthlib.flow import InstalledAppFlow

SCOPES = ["https://www.googleapis.com/auth/youtube.upload", "https://www.googleapis.com/auth/youtube.readonly"]

def generate_token(client_secret_file, token_output_path):
    flow = InstalledAppFlow.from_client_secrets_file(client_secret_file, SCOPES)
    creds = flow.run_local_server(port=0)
    with open(token_output_path, "w") as token:
        token.write(creds.to_json())
    print(f"Da luu token thanh cong vao: {token_output_path}")

if __name__ == "__main__":
    print("Script san sang.")
