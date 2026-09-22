# Pexels API fetcher for TNT Media - permanent module (2026-09-12)
import urllib.request,json,os
KEY=os.environ.get("PEXELS_API_KEY") or open(os.path.join(os.path.dirname(__file__),"..",".env")).read().split("PEXELS_API_KEY=")[1].split(chr(10))[0].strip()
H={"Authorization":KEY,"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
def search(query,per=6,orientation="portrait"):
 u="https://api.pexels.com/videos/search?query="+query.replace(" ","%20")+"&per_page="+str(per)+"&orientation="+orientation
 return json.loads(urllib.request.urlopen(urllib.request.Request(u,headers=H),timeout=30).read())
def urls(query,per=6):
 d=search(query,per)
 vs=d.get("videos",[])
 allf=[f for v in vs for f in v.get("video_files",[])]
 good=[f for f in allf if f.get("file_type")=="video/mp4" and f.get("height",0)>=600]
 return [f["link"] for f in good]
def download(url,dest):
 data=urllib.request.urlopen(urllib.request.Request(url,headers=H),timeout=60).read()
 open(dest,"wb").write(data)
 return dest