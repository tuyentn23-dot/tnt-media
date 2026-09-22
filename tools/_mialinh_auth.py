import os, sys, pickle
sys.path.insert(0, os.getcwd())
from google_auth_oauthlib.flow import InstalledAppFlow

SCOPES = [
 "https://www.googleapis.com/auth/youtube.upload",
 "https://www.googleapis.com/auth/youtube.readonly",
]

client_secret = "client_secret.json"
token_out = os.path.join("channels", "Mialinhcute", "token.pickle")

flow = InstalledAppFlow.from_client_secrets_file(client_secret, SCOPES)
creds = flow.run_local_server(port=0, open_browser=True)

with open(token_out, "wb") as f:
 pickle.dump(creds, f)
print("SAVED", token_out)