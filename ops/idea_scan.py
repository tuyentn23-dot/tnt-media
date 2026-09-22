import sys, json
sys.path.insert(0,"ops")
import daily_trend as T
kws=["sự thật thú vị","bạn có biết","khoa học kỳ thú","động vật","vũ trụ","cơ thể người"]
all=[]
for kw in kws:
 r=T.search_kw(kw,5)
 all.append({"kw":kw,"items":r})
json.dump(all,open("memory/idea_scan.json","w",encoding="utf-8"),ensure_ascii=False,indent=1)
print("SCANNED",len(all))
