import sys,os,json,time,sqlite3
sys.stdout.reconfigure(encoding="utf-8",errors="replace")
sys.path.insert(0,".")
from ops import os_publish as OP
sel=json.load(open("publish_list.json",encoding="utf-8"))
results=[]
for ch,files in sel.items():
	OP.set_channel(ch)
	print("=== ",ch,OP.active_channel())
	for f in files:
		p=os.path.abspath(os.path.join("output",f))
		base=os.path.splitext(f)[0]
		title=base.replace(""," ")[:100]
		desc="#shorts #"+ch
		tags=["shorts","viral",ch]
		r=OP.publish(p,title,description=desc,tags=tags,topic=base)
		msg=str(r.get("error") or r.get("youtube_id") or "ok")
		print(" ",f,msg)
		results.append({"channel":ch,"file":f,"result":r})
		time.sleep(2)
json.dump(results,open("_publish_result.json","w"),ensure_ascii=False,indent=2,default=str)
ok=sum(1 for x in results if x["result"].get("ok"))
print("DONE ",ok,"/",len(results))
