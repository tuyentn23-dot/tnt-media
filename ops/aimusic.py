# -- coding: utf-8 --
"""AI music pipeline."""
import os, io, sys, json, time, subprocess, urllib.request, urllib.error
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)
OUTDIR = os.path.join(ROOT, "output")
ASSETS = os.path.join(ROOT, "projects", "aimusic", "assets")
FFMPEG = os.path.join(ROOT, "tools", "ffmpeg.exe")

def _env():
	d={}
	p=os.path.join(ROOT,".env")
	if os.path.exists(p):
		for line in io.open(p,encoding="utf-8"):
			line=line.strip()
			if line and not line.startswith("#") and "=" in line:
				k,v=line.split("=",1)
				d[k.strip()]=v.strip()
	return d

ENV=_env()
OPENAI_KEY=ENV.get("OPENAI_API_KEY","")

def log(*a):
	print("[aimusic]", *a, flush=True)

def _openai(path, payload, timeout=300):
	req=urllib.request.Request("https://api.openai.com/v1/"+path,
		data=json.dumps(payload).encode("utf-8"),
		headers={"Authorization":"Bearer "+OPENAI_KEY, "Content-Type":"application/json"})
	last=None
	for i in range(3):
		try:
			r=urllib.request.urlopen(req,timeout=timeout)
			return json.loads(r.read().decode("utf-8"))
		except Exception as e:
			last=e
			time.sleep(4)
	raise RuntimeError("openai "+path+" failed: "+str(last))

def gpt(prompt, system=None, model="gpt-4o", max_tokens=4000):
	msgs=[]
	if system:
		msgs.append({"role":"system","content":system})
	msgs.append({"role":"user","content":prompt})
	payload={"model":model,"messages":msgs,"temperature":0.9,"max_tokens":max_tokens}
	r=_openai("chat/completions",payload)
	return r["choices"][0]["message"]["content"]