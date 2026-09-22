import sys, os
sys.path.insert(0,".")
from ops.publish_one import upload, record
path=sys.argv[1]
title=sys.argv[2]
desc=sys.argv[3]
tags=sys.argv[4].split(",") if len(sys.argv)>4 else ["shorts"]
vid=upload(path, title, desc, tags)
record({"youtube_id": vid, "title": title, "file": path})
print("PUBLISHED https://youtube.com/shorts/"+vid)
