import sys,os,sqlite3,subprocess,json
sys.stdout.reconfigure(encoding="utf-8",errors="replace")
sys.path.insert(0,".")
FF=os.path.join("tools","ffmpeg.exe")
c=sqlite3.connect("state/pipeline.db")
c.row_factory=sqlite3.Row
rows=c.execute("SELECT file_path FROM publications WHERE youtube_id IS NOT NULL").fetchall()
pub=set(os.path.basename(r["file_path"]) for r in rows if r["file_path"])
print("published:",len(pub))
out=os.listdir("output")
chans={"vilevi5676":[],"Mialinhcute":[]}
for f in out:
	if not f.endswith(".mp4") or f in pub: continue
	p=os.path.join("output",f)
	if os.path.getsize(p)<300000: continue
	if f.lower().startswith("mialinh"): chans["Mialinhcute"].append(f)
	elif "vilevi" in f.lower(): chans["vilevi5676"].append(f)
sel={}
for ch,lst in chans.items():
	lst.sort(key=lambda x: os.path.getmtime(os.path.join("output",x)), reverse=True)
	picked=[]
	for f in lst:
		p=os.path.join("output",f)
		r=subprocess.run([FF,"-i",p],capture_output=True,text=True,encoding="utf-8",errors="replace")
		au="Audio:" in r.stderr
		if au: picked.append(f)
		if len(picked)>=4: break
	sel[ch]=picked
	print(ch,"picked:",len(picked))
	for f in picked: print(" ",f)
json.dump(sel,open("_selected.json","w"),ensure_ascii=False,indent=2)
print("SAVED")
