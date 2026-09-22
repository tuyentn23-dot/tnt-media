# oauth_analytics.py - lay token YouTube Analytics (chay 1 lan)
import os, sys, pickle
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
ROOT = os.path.dirname(os.path.abspath(__file__))
SCOPES = ["https://www.googleapis.com/auth/youtube", "https://www.googleapis.com/auth/yt-analytics.readonly"]
CLIENT = os.path.join(ROOT,"client_secret.json")
TOKEN = os.path.join(ROOT,"token.pickle")
def main():
	if not os.path.exists(CLIENT):
		print("MISSING client_secret.json"); return 1
	print("Dang mo trinh duyet dang nhap Google...")
	flow = InstalledAppFlow.from_client_secrets_file(CLIENT, SCOPES)
	creds = flow.run_local_server(port=0)
	pickle.dump(creds, open(TOKEN,"wb"))
	print("OK scopes:", creds.scopes)
	return 0
if __name__ == "__main__":
	raise SystemExit(main())