# yt_analytics.py - doc view/CTR/retention that su tu YouTube Analytics API
import os, sys, io, json, pickle, time
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)
TOKEN = os.path.join(ROOT,"token.pickle")
CACHE = os.path.join(ROOT,"memory","yt_analytics.json")

def _creds():
	from google.oauth2.credentials import Credentials
	if os.path.exists(TOKEN):
		try: return pickle.load(open(TOKEN,"rb"))
		except Exception: pass
	return None

def fetch(days=28):
	c=_creds()
	if not c: return {"ok":False,"error":"no token"}
	try:
		from googleapiclient.discovery import build
		yta=build("youtubeAnalytics","v2",credentials=c)
		end=time.strftime("%Y-%m-%d")
		start=time.strftime("%Y-%m-%d",time.localtime(time.time()-days*86400))
		resp=yta.reports().query(ids="channel==MINE",startDate=start,endDate=end,metrics="views,estimatedMinutesWatched,averageViewDuration",dimensions="video",sort="-views",maxResults=50).execute()
		io.open(CACHE,"w",encoding="utf-8").write(json.dumps(resp,ensure_ascii=False,indent=2))
		return {"ok":True,"rows":resp.get("rows",[]),"headers":[h.get("name") for h in resp.get("columnHeaders",[])]}
	except Exception as e:
		return {"ok":False,"error":str(e)[:200]}

def cached():
	try: return json.load(io.open(CACHE,encoding="utf-8"))
	except Exception: return {}