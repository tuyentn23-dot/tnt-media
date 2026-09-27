import sys,os,sqlite3,subprocess,json
sys.stdout.reconfigure(encoding="utf-8",errors="replace")
sys.path.insert(0,".")
FF=os.path.join("tools","ffmpeg.exe")
c=sqlite3.connect("state/pipeline.db")
c.row_factory=sqlite3.Row
pub=set(os.path.basename(r["file_path"]) for r in c.execute("SELECT file_path FROM publications WHERE youtube_id IS NOT NULL").fetchall() if r["file_path"])
out=[f for f in os.listdir("output") if f.endswith(".mp4") and f not in pub and os.path.getsize(os.path.join("output",f))>300000]
def info(p):
	r=subprocess.run([FF,"-i",p],capture_output=True,text=True,encoding="utf-8",errors="replace")
	return "Audio:" in r.stderr
vi=[f for f in out if "vilevi" in f.lower() and info(os.path.join("output",f))]
mi=[f for f in out if f.lower().startswith("mialinh") and info(os.path.join("output",f))]
vi.sort(key=lambda x: os.path.getmtime(os.path.join("output",x)), reverse=True)
mi.sort(key=lambda x: os.path.getmtime(os.path.join("output",x)), reverse=True)
sel={"vilevi5676":vi[:4],"Mialinhcute":mi[:4]}
json.dump(sel,open("_publish_list.json","w"),ensure_ascii=False,indent=2)
for k,v in sel.items():
	print(k,len(v))
	for f in v: print(" ",f)
