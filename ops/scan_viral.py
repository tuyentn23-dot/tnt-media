import sys, glob, json
sys.path.insert(0,".")
from ops.viral_engine import analyze
fs=glob.glob("output/Tự làm/viral*.mp4")
r=[]
for f in fs:
 try:
      a=analyze(f)
      r.append([round(a["hook_motion"],1),a["viral_score"],f.split(chr(92))[-1]])
 except:
      pass
r.sort(reverse=True)
json.dump(r[:10],open("output/_vtop.json","w"))
print(len(r))
