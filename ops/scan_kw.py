import sys
sys.path.insert(0,"ops")
import daily_trend as T
for kw in ["bí ẩn","sự thật"]:
 print("===",kw)
 r=T.search_kw(kw,6)
 for v in r: print(v["views"],v["title"][:50])
