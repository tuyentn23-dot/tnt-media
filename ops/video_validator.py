# video_validator.py - validate video
import subprocess, os, re
FF=os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),"tools","ffmpeg.exe")
def probe(path):
     if not os.path.exists(path): return {"ok":False,"err":"not found"}
     if os.path.getsize(path)<10000: return {"ok":False,"err":"too small"}
     r=subprocess.run([FF,"-i",path],stdout=subprocess.PIPE,stderr=subprocess.STDOUT,text=True)
     o=r.stdout
     hv="Video:" in o; ha="Audio:" in o
     return {"ok":hv,"video":hv,"audio":ha}

def clean(folder):
    import glob
    bad=[]
    good=[]
    for f in glob.glob(os.path.join(folder,"*.mp4")):
        p=probe(f)
        if p.get("ok"): good.append(f)
        else: bad.append(f)
    return {"good":len(good),"bad":len(bad),"badlist":bad[:10]}
