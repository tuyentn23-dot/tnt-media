# remix_engine.py - bat chuoc format viral + Viet hoa thanh concept goc
import os, sys, json
from datetime import date
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0,ROOT)
MEM=os.path.join(ROOT,"memory")
FORMATS={
    "music":{"pattern":"hook 3s + doan hook + beat drop","vn":"Nhac Viet remix + visual dep + lyric dong bo"},
    "story":{"pattern":"cau hoi gay to mo + tiet lo + twist","vn":"Ke chuyen Viet + giong cam xuc + footage khop"},
    "fact":{"pattern":"su that soc + 3 chi tiet + payoff","vn":"Kien thuc Viet hoa + caption ro + hinh dong"},
    "satisfying":{"pattern":"chuyen dong manh + loop muot + ASMR","vn":"Visual dep + nhac nhe + caption tam trang"},
}

def latest_trend():
    import glob
    fs=sorted(glob.glob(os.path.join(MEM,"trends","trend_*.json")))
    if not fs: return dict()
    return json.load(open(fs[0],encoding="utf-8"))

def classify(title):
    t=title.lower()
    if any(k in t for k in ["music","remix","cover","mv"]): return "music"
    if any(k in t for k in ["100 days","story"]): return "story"
    if any(k in t for k in ["fact","why","secret"]): return "fact"
    return "satisfying"

def plan():
    d=latest_trend()
    tops=d.get("top_by_views",[])
    rows=[]
    for v in tops[:6]:
        fmt=classify(v.get("title",""))
        f=FORMATS.get(fmt,FORMATS["satisfying"])
        rows.append({"inspire":v.get("title")[:50],"format":fmt,"pattern":f["pattern"],"vn_angle":f["vn"]})
    return rows

def save(rows):
    os.makedirs(os.path.join(MEM,"plans"),exist_ok=True)
    p=os.path.join(MEM,"plans","plan_"+date.today().isoformat()+".json")
    json.dump(rows,open(p,"w",encoding="utf-8"),ensure_ascii=False,indent=2)
    return p

if __name__=="__main__":
    rows=plan()
    p=save(rows)
    for r in rows: print(r["format"],r["vn_angle"])
    print("SAVED",p)
