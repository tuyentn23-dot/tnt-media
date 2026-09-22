import sys, glob, json, os
sys.path.insert(0,".")
from ops.viral_engine import analyze
files=glob.glob("output/Tự làm/*.mp4")
ok=[]
for f in files:
 try:
      a=analyze(f)
      ok.append([os.path.basename(f),a["viral_score"]])
 except:
      pass
ok.sort(key=lambda x:-x[1])
json.dump(ok[:15],open("output/_top65.json","w"))
print(len(ok))
