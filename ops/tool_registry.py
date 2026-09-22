# tool_registry.py
import os, json
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OPS=os.path.join(ROOT,"ops")
OUT=os.path.join(ROOT,"memory","tool_registry.json")
KW={"video":"video make story content render clip compose","publish":"publish upload youtube","seo":"seo trend idea remix","analytics":"analytic manager perf track","audio":"audio music tts voice","quality":"valid quality gate score scan clean","footage":"pexels footage library"}
def classify(name):
    n=name.lower()
    for cat,kws in KW.items():
      if any(k in n for k in kws.split()): return cat
    return "other"
def scan():
    import ast
    tools=[]
    for f in sorted(os.listdir(OPS)):
      if not f.endswith(".py"): continue
      path=os.path.join(OPS,f)
      doc=""
      try:
        m=ast.parse(open(path,encoding="utf-8").read())
        doc=(ast.get_docstring(m) or "").split(chr(10))[0][:80]
      except: pass
      tools.append({"file":f,"cat":classify(f),"doc":doc})
    return tools
def build():
    tools=scan()
    from collections import Counter
    cats=Counter(t["cat"] for t in tools)
    reg={"total":len(tools),"by_cat":dict(cats),"tools":tools}
    json.dump(reg,open(OUT,"w",encoding="utf-8"),ensure_ascii=False,indent=1)
    return reg
if __name__=="__main__":
    r=build()
    print("TOTAL",r["total"])
    for c,n in r["by_cat"].items(): print(c,n)
