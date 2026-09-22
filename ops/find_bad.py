import sys, glob, os, json
sys.path.insert(0,".")
from ops.video_validator import probe
folder=sys.argv[1] if len(sys.argv)>1 else "output/Tự làm"
fs=glob.glob(os.path.join(folder,"*.mp4"))
bad=[f for f in fs if not probe(f).get("ok")]
json.dump(bad,open("output/_bad_videos.json","w"))
print("total",len(fs),"bad",len(bad))
