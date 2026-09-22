import sys, json
sys.path.insert(0,"ops")
import daily_trend as T
out={}
for kw in ["sự thật","bạn có biết","khoa học","động vật"]:
    try:
      out[kw]=T.search_kw(kw,8)
    except:
      pass
json.dump(out,open("memory/viral_samples.json","w",encoding="utf-8"),ensure_ascii=False,indent=1)
print("saved")
