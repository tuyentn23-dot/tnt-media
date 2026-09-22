import json, shutil, os
bad=json.load(open("output/_bad_videos.json",encoding="utf-8"))
os.makedirs("_trash/bad_videos",exist_ok=True)
n=0
for b in bad:
    try:
      if os.path.exists(b): shutil.move(b,"_trash/bad_videos/"+os.path.basename(b)); n=n+1
    except Exception as e:
      print("skip")
print("moved",n)
