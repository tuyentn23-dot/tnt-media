# make_client_secret.py - tao client_secret.json tu .env
import os, io, sys, json
ROOT = os.path.dirname(os.path.abspath(__file__))
def env():
	d={}
	for line in io.open(os.path.join(ROOT,".env"),encoding="utf-8"):
		line=line.strip()
		if line and not line.startswith("#") and "=" in line:
			k,v=line.split("=",1); d[k.strip()]=v.strip()
	return d
def main():
	e=env()
	cid=e.get("YOUTUBE_CLIENT_ID","")
	cs=e.get("YOUTUBE_CLIENT_SECRET","")
	if not cid or not cs:
		print("Thieu YOUTUBE_CLIENT_ID/SECRET trong .env"); return 1
	doc={"installed":{"client_id":cid,"client_secret":cs,"auth_uri":"https://accounts.google.com/o/oauth2/auth","token_uri":"https://oauth2.googleapis.com/token","redirect_uris":["http://localhost"]}}
	io.open(os.path.join(ROOT,"client_secret.json"),"w",encoding="utf-8").write(json.dumps(doc,indent=2))
	print("Da tao client_secret.json")
	return 0
if __name__ == "__main__":
	raise SystemExit(main())