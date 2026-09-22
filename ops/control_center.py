# TNT Media 24/7 Control Center v3.0.0
import os, json, glob, shutil, time, subprocess, sys, threading
from datetime import datetime
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "output")
LIB = os.path.join(ROOT, "library")
MEM = os.path.join(ROOT, "memory")
TRASH = os.path.join(ROOT, "_trash")
PUB = os.path.join(MEM, "published.json")
PY = sys.executable
try:
	from ops import autopilot as _ap
except Exception:
	_ap = None
try:
	from ops import evolve as _ev
except Exception:
	_ev = None
try:
	from ops import yt_analytics as _ya
except Exception:
	_ya = None
except Exception:
	_ev = None
def jload(path, default=None):
    try:
        return json.load(open(path, encoding="utf-8"))
    except Exception:
        return default if default is not None else {}
def jsave(path, data):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    json.dump(data, open(path, "w", encoding="utf-8"), indent=2)
def human(n):
    for u in ["B", "KB", "MB", "GB"]:
        if n < 1024:
            return str(round(n, 1)) + u
        n /= 1024
    return str(round(n, 1)) + "TB"
def file_info(path):
    try:
        st = os.stat(path)
        return {"path": os.path.relpath(path, ROOT), "size": st.st_size, "size_h": human(st.st_size), "mtime": datetime.fromtimestamp(st.st_mtime).isoformat()}
    except Exception:
        return None
def published():
    return jload(PUB, {"videos": []})
def mark_published(rec):
    d = published()
    d.setdefault("videos", []).append(rec)
    jsave(PUB, d)
def all_output_videos():
    res = []
    for path in glob.glob(os.path.join(OUT, "*.mp4")):
        i = file_info(path)
        if i:
            res.append(i)
    return sorted(res, key=lambda x: x["mtime"], reverse=True)
def library_stats():
    out = {}
    for t in sorted(os.listdir(LIB)):
        d = os.path.join(LIB, t)
        if not os.path.isdir(d):
            continue
        m = jload(os.path.join(d, "_manifest.json"), [])
        best = max([e.get("score", 0) for e in m]) if m else 0
        out[t] = {"clips": len(m), "best_score": best}
    return out
def trash_path(path):
    os.makedirs(TRASH, exist_ok=True)
    dest = os.path.join(TRASH, str(int(time.time())) + "_" + os.path.basename(path))
    shutil.move(path, dest)
    return dest
def cleanup_junk():
    removed = []
    patterns = ["*TEMP_MPY*", "*.tmp", "*_mid.mp4", "tiny_*.mp4", "*_test*.mp4"]
    for pat in patterns:
        for path in glob.glob(os.path.join(OUT, pat)):
            removed.append(os.path.relpath(trash_path(path), ROOT))
    for path in glob.glob(os.path.join(ROOT, "*.py")) + glob.glob(os.path.join(ROOT, "*.txt")) + glob.glob(os.path.join(ROOT, "*.json")):
        removed.append(os.path.relpath(trash_path(path), ROOT))
    return removed
def disk_usage():
    total = 0
    for root, _, files in os.walk(ROOT):
        for f in files:
            try:
                total += os.path.getsize(os.path.join(root, f))
            except Exception:
                pass
    return {"bytes": total, "human": human(total)}
def run_script(rel, args=None):
    cmd = [PY, rel] + (args or [])
    env = dict(os.environ)
    env["PYTHONPATH"] = ROOT
    try:
        r = subprocess.run(cmd, cwd=ROOT, capture_output=True, text=True, timeout=600, env=env)
        return {"ok": r.returncode == 0, "code": r.returncode, "out": r.stdout[-2000:], "err": r.stderr[-1000:]}
    except Exception as e:
        return {"ok": False, "error": str(e)}
AUTO_STATE = os.path.join(MEM, 'automation_state.json')
def _load_state():
    try:
        import json
        d = json.load(open(AUTO_STATE, encoding='utf-8'))
        return dict(auto_publish=bool(d.get('auto_publish')), auto_scan=bool(d.get('auto_scan')), auto_evaluate=bool(d.get('auto_evaluate')), auto_upgrade=bool(d.get('auto_upgrade')))
    except Exception:
        return dict(auto_publish=False, auto_scan=False, auto_evaluate=False, auto_upgrade=False)
def _save_state():
    try:
        import json
        json.dump(STATE, open(AUTO_STATE, 'w', encoding='utf-8'))
    except Exception:
        pass
STATE = _load_state()
LOCK = threading.Lock()
def worker_loop():
    while True:
        try:
            if STATE["auto_scan"]:
                run_script("ops/real_footage_pipeline.py", ["--topics", "food,coffee,water,fire", "--limit", "2"])
            if STATE["auto_evaluate"]:
                run_script("ops/analytics_aggregator.py")
            if STATE["auto_publish"]:
                run_script("ops/autopublish_runner.py")
            run_script("ops/cleanup.py")
            if STATE["auto_upgrade"]:
                run_script("ops/auto_evolution.py")
        except Exception:
            pass
        time.sleep(120)
def start_worker():
    t = threading.Thread(target=worker_loop, daemon=True)
    t.start()
    return t
try:
    from fastapi import FastAPI, HTTPException
    from fastapi.responses import HTMLResponse, JSONResponse
    HAVE_FASTAPI = True
except ImportError:
    HAVE_FASTAPI = False
app = FastAPI(title="TNT Media Control Center", version="3.0.0") if HAVE_FASTAPI else None

# TNT Media OS mount (/os)
try:
    from os_app.router import router as _os_router
    app.include_router(_os_router)
except Exception as _e:
    pass
def status():
    vids = all_output_videos()
    pv = published(); pub = pv.get("videos", []) if isinstance(pv, dict) else pv
    return {"time": datetime.now().isoformat(), "videos": len(vids), "published": len(pub), "library": library_stats(), "disk": disk_usage(), "automation": dict(STATE)}
def videos():
 pv = published()
 pub = pv.get("videos", []) if isinstance(pv, dict) else pv
 return {"videos": all_output_videos(), "published": pub}
def delete_video(rel):
    full = os.path.join(ROOT, rel)
    if not os.path.exists(full):
        return {"ok": False, "error": "not found"}
    dest = trash_path(full)
    return {"ok": True, "moved_to": os.path.relpath(dest, ROOT)}
def set_automation(flag, value):
    if flag not in STATE:
        return {"ok": False, "error": "unknown flag"}
    STATE[flag] = bool(value)
    _save_state()
    return {"ok": True, "automation": dict(STATE)}
def regenerate_index():
    vids = all_output_videos()
    jsave(os.path.join(MEM, "output_index.json"), {"videos": vids})
    return {"ok": True, "count": len(vids)}

def add_published(youtube_id, topic=None, score=None):
    d = published()
    d.setdefault("videos", []).append({"youtube_id": youtube_id, "topic": topic, "viral_score": score, "published_at": datetime.now().isoformat()})
    jsave(PUB, d)
    return {"ok": True, "total": len(d["videos"])}

def channel_real():
    return jload(os.path.join(MEM,"channel_real.json"),{})
def channels_list():
    # Đọc trực tiếp từ file cấu hình đa kênh channels_config.json
    return jload(os.path.join(MEM, "channels_config.json"), {"channels": [], "active": None})

def analytics():
    perf = jload(os.path.join(MEM,"performance.json"),[])
    best={}
    for v in perf:
        vid=v.get("id")
        if not vid: continue
        c=best.get(vid)
        if c is None or int(v.get("views",0))>int(c.get("views",0)): best[vid]=v
    rows=list(best.values())
    return {"views":sum(int(v.get("views",0)) for v in rows),"likes":sum(int(v.get("likes",0)) for v in rows),"comments":sum(int(v.get("comments",0)) for v in rows),"tracked":len(rows),"duplicates_removed":len(perf)-len(rows)}

def content_db():
    d=jload(os.path.join(MEM,"content_db.json"),{})
    return {"whatif":len(d.get("whatif",[])),"facts":len(d.get("facts",[]))}

def activity():
    return jload(os.path.join(MEM,"pdca_log.json"),{"events":[]}).get("events",[])[-20:]

@app.get("/api/autopilot")
def autopilot_status():
	return _ap.status() if _ap else {"error":"no autopilot"}

@app.post("/api/autopilot/enable")
def autopilot_enable(flag: int = 1):
	return _ap.set_enabled(bool(flag)) if _ap else {"error":"no autopilot"}

@app.post("/api/autopilot/run")
def autopilot_run():
	return _ap.run_cycle() if _ap else {"error":"no autopilot"}

@app.post("/api/autopilot/cfg")
def autopilot_cfg(interval_min: int = None, batch: int = None):
	c=_ap._cfg() if _ap else {}
	if interval_min is not None: c["interval_min"]=interval_min
	if batch is not None: c["batch"]=batch
	if _ap: _ap._save(c)
	return c

@app.get("/api/evolve")
def evolve_status():
	return _ev._load() if _ev else {"error":"no evolve"}

@app.post("/api/evolve/run")
def evolve_run():
	return _ev.run_once() if _ev else {"error":"no evolve"}

@app.get("/api/evolve/suggest")
def evolve_suggest():
	return _ev.suggest() if _ev else {"error":"no evolve"}

@app.get("/api/analytics")
def analytics():
	return _ya.cached() if _ya else {"error":"no analytics"}

@app.post("/api/analytics/fetch")
def analytics_fetch():
	return _ya.fetch(28) if _ya else {"error":"no analytics"}

HTML = __import__("base64").b64decode("PCFkb2N0eXBlIGh0bWw+CjxodG1sIGxhbmc9InZpIj4KPGhlYWQ+CiAgPG1ldGEgY2hhcnNldD0idXRmLTgiPgogIDx0aXRsZT5UTlQgTWVkaWEgLSBNdWx0aS1DaGFubmVsIENvbnRyb2wgQ2VudGVyPC90aXRsZT4KICA8c3R5bGU+CiAgICA6cm9vdCB7IC0tYmc6ICMwZDExMTc7IC0tY2FyZDogIzE2MWIyMjsgLS1ib3JkZXI6ICMzMDM2M2Q7IC0tdGV4dDogI2U2ZWRmMzsgLS1hY2NlbnQ6ICMyMzg2MzY7IC0tYWNjZW50LWhvdmVyOiAjMmVhMDQzOyAtLWJsdWU6ICMxZjZmZWI7IC0tcmVkOiAjZGEzNjMzOyB9CiAgICBib2R5IHsgZm9udC1mYW1pbHk6IC1hcHBsZS1zeXN0ZW0sIEJsaW5rTWFjU3lzdGVtRm9udCwgIlNlZ29lIFVJIiwgUm9ib3RvLCBzYW5zLXNlcmlmOyBiYWNrZ3JvdW5kOiB2YXIoLS1iZyk7IGNvbG9yOiB2YXIoLS10ZXh0KTsgbWFyZ2luOiAwOyBwYWRkaW5nOiAyMHB4OyB9CiAgICAuY29udGFpbmVyIHsgbWF4LXdpZHRoOiAxMjAwcHg7IG1hcmdpbjogYXV0bzsgfQogICAgaGVhZGVyIHsgZGlzcGxheTogZmxleDsganVzdGlmeS1jb250ZW50OiBzcGFjZS1iZXR3ZWVuOyBhbGlnbi1pdGVtczogY2VudGVyOyBib3JkZXItYm90dG9tOiAxcHggc29saWQgdmFyKC0tYm9yZGVyKTsgcGFkZGluZy1ib3R0b206IDE1cHg7IG1hcmdpbi1ib3R0b206IDIwcHg7IH0KICAgIGgxIHsgZm9udC1zaXplOiAyMnB4OyBjb2xvcjogIzU4YTZmZjsgbWFyZ2luOiAwOyB9CiAgICAuZ3JpZCB7IGRpc3BsYXk6IGdyaWQ7IGdyaWQtdGVtcGxhdGUtY29sdW1uczogMWZyIDFmcjsgZ2FwOiAyMHB4OyB9CiAgICBAbWVkaWEgKG1heC13aWR0aDogODAwcHgpIHsgLmdyaWQgeyBncmlkLXRlbXBsYXRlLWNvbHVtbnM6IDFmcjsgfSB9CiAgICAuY2FyZCB7IGJhY2tncm91bmQ6IHZhcigtLWNhcmQpOyBib3JkZXI6IDFweCBzb2xpZCB2YXIoLS1ib3JkZXIpOyBib3JkZXItcmFkaXVzOiAxMnB4OyBwYWRkaW5nOiAyMHB4OyBtYXJnaW4tYm90dG9tOiAyMHB4OyBib3gtc2hhZG93OiAwIDRweCAxMnB4IHJnYmEoMCwwLDAsMC4zKTsgfQogICAgaDIgeyBmb250LXNpemU6IDE2cHg7IG1hcmdpbi10b3A6IDA7IGJvcmRlci1ib3R0b206IDFweCBzb2xpZCB2YXIoLS1ib3JkZXIpOyBwYWRkaW5nLWJvdHRvbTogOHB4OyBjb2xvcjogIzhiOTQ5ZTsgfQogICAgLmJ0biB7IGJhY2tncm91bmQ6IHZhcigtLWFjY2VudCk7IGNvbG9yOiAjZmZmOyBib3JkZXI6IDA7IGJvcmRlci1yYWRpdXM6IDZweDsgcGFkZGluZzogMTBweCAxOHB4OyBmb250LXdlaWdodDogNjAwOyBjdXJzb3I6IHBvaW50ZXI7IG1hcmdpbjogNHB4OyB9CiAgICAuYnRuOmhvdmVyIHsgYmFja2dyb3VuZDogdmFyKC0tYWNjZW50LWhvdmVyKTsgfQogICAgLmJ0bi5yZWQgeyBiYWNrZ3JvdW5kOiB2YXIoLS1yZWQpOyB9CiAgICAuYnRuLmJsdWUgeyBiYWNrZ3JvdW5kOiB2YXIoLS1ibHVlKTsgfQogICAgdGFibGUgeyB3aWR0aDogMTAwJTsgYm9yZGVyLWNvbGxhcHNlOiBjb2xsYXBzZTsgbWFyZ2luLXRvcDogMTBweDsgfQogICAgdGgsIHRkIHsgdGV4dC1hbGlnbjogbGVmdDsgcGFkZGluZzogMTBweDsgYm9yZGVyLWJvdHRvbTogMXB4IHNvbGlkIHZhcigtLWJvcmRlcik7IGZvbnQtc2l6ZTogMTRweDsgfQogICAgdGggeyBjb2xvcjogIzhiOTQ5ZTsgfQogICAgLmJhZGdlIHsgcGFkZGluZzogNHB4IDhweDsgYm9yZGVyLXJhZGl1czogNHB4OyBmb250LXNpemU6IDEycHg7IGZvbnQtd2VpZ2h0OiA2MDA7IH0KICAgIC5iYWRnZS5vbiB7IGJhY2tncm91bmQ6IHJnYmEoMzUsMTM0LDU0LDAuMik7IGNvbG9yOiAjM2ZiOTUwOyB9CiAgICAuYmFkZ2Uub2ZmIHsgYmFja2dyb3VuZDogcmdiYSgyMTgsNTQsNTEsMC4yKTsgY29sb3I6ICNmODUxNDk7IH0KICA8L3N0eWxlPgo8L2hlYWQ+Cjxib2R5PgogIDxkaXYgY2xhc3M9ImNvbnRhaW5lciI+CiAgICA8aGVhZGVyPgogICAgICA8aDE+8J+OrCBUTlQgTWVkaWEgLSBNdWx0aS1DaGFubmVsIENvbnRyb2wgQ2VudGVyPC9oMT4KICAgICAgPGRpdj4KICAgICAgICA8YnV0dG9uIGNsYXNzPSJidG4gYmx1ZSIgb25jbGljaz0iZmV0Y2goJy9hcGkvdHJpZ2dlcicsIHttZXRob2Q6J1BPU1QnfSkudGhlbigoKT0+YWxlcnQoJ8SQw6Mga8OtY2ggaG/huqF0IGNodSBr4buzIScpKSI+4pqhIENo4bqheSBuZ2F5IDEgY2h1IGvhu7M8L2J1dHRvbj4KICAgICAgPC9kaXY+CiAgICA8L2hlYWRlcj4KCiAgICA8ZGl2IGNsYXNzPSJncmlkIj4KICAgICAgPCEtLSBUcuG6oW5nIHRow6FpIEF1dG9waWxvdCAtLT4KICAgICAgPGRpdiBjbGFzcz0iY2FyZCI+CiAgICAgICAgPGgyPvCfpJYgVHLhuqFuZyB0aMOhaSBU4buxIMSR4buZbmcgaMOzYSAoQXV0b3BpbG90KTwvaDI+CiAgICAgICAgPGRpdiBpZD0ic3RhdHVzLWJveCIgc3R5bGU9Im1hcmdpbi1ib3R0b206IDE1cHg7IGZvbnQtc2l6ZTogMTVweDsiPsSQYW5nIHThuqNpIHRy4bqhbmcgdGjDoWkuLi48L2Rpdj4KICAgICAgICA8YnV0dG9uIGNsYXNzPSJidG4iIG9uY2xpY2s9InRvZ2dsZUF1dG8odHJ1ZSkiPkLhuq10IEF1dG9waWxvdDwvYnV0dG9uPgogICAgICAgIDxidXR0b24gY2xhc3M9ImJ0biByZWQiIG9uY2xpY2s9InRvZ2dsZUF1dG8oZmFsc2UpIj5U4bqvdCBBdXRvcGlsb3Q8L2J1dHRvbj4KICAgICAgPC9kaXY+CgogICAgICA8IS0tIFRo4buRbmcga8OqIGjhu4cgdGjhu5FuZyAtLT4KICAgICAgPGRpdiBjbGFzcz0iY2FyZCI+CiAgICAgICAgPGgyPvCfk4ogVOG7lW5nIHF1YW4gSOG7hyB0aOG7kW5nPC9oMj4KICAgICAgICA8ZGl2IGlkPSJzdGF0cy1ib3giIHN0eWxlPSJmb250LXNpemU6IDE0cHg7IGxpbmUtaGVpZ2h0OiAxLjY7Ij7EkGFuZyB04bqjaSBk4buvIGxp4buHdS4uLjwvZGl2PgogICAgICA8L2Rpdj4KICAgIDwvZGl2PgoKICAgIDwhLS0gUXXhuqNuIGzDvSBrw6puaCBZb3VUdWJlIC0tPgogICAgPGRpdiBjbGFzcz0iY2FyZCI+CiAgICAgIDxoMj7wn5O6IERhbmggc8OhY2ggS8OqbmggWW91VHViZSBRdeG6o24gbMO9PC9oMj4KICAgICAgPGRpdiBzdHlsZT0ib3ZlcmZsb3cteDogYXV0bzsiPgogICAgICAgIDx0YWJsZT4KICAgICAgICAgIDx0aGVhZD4KICAgICAgICAgICAgPHRyPgogICAgICAgICAgICAgIDx0aD5Uw6puIEvDqm5oPC90aD4KICAgICAgICAgICAgICA8dGg+Q2jhu6cgxJHhu4EgKE5pY2hlKTwvdGg+CiAgICAgICAgICAgICAgPHRoPlThuqduIHN14bqldDwvdGg+CiAgICAgICAgICAgICAgPHRoPlRy4bqhbmcgdGjDoWk8L3RoPgogICAgICAgICAgICA8L3RyPgogICAgICAgICAgPC90aGVhZD4KICAgICAgICAgIDx0Ym9keSBpZD0iY2hhbm5lbHMtdGFibGUiPgogICAgICAgICAgICA8dHI+PHRkIGNvbHNwYW49IjQiPsSQYW5nIHThuqNpIGRhbmggc8OhY2gga8OqbmguLi48L3RkPjwvdHI+CiAgICAgICAgICA8L3Rib2R5PgogICAgICAgIDwvdGFibGU+CiAgICAgIDwvZGl2PgogICAgPC9kaXY+CgogICAgPCEtLSBWaWRlbyBn4bqnbiDEkcOieSAtLT4KICAgIDxkaXYgY2xhc3M9ImNhcmQiPgogICAgICA8aDI+8J+Onu+4jyBWaWRlbyBH4bqnbiDEkMOieTwvaDI+CiAgICAgIDxkaXYgaWQ9InJlY2VudC12aWRlb3MiIHN0eWxlPSJmb250LXNpemU6IDE0cHg7Ij7EkGFuZyBj4bqtcCBuaOG6rXQgZGFuaCBzw6FjaCB2aWRlby4uLjwvZGl2PgogICAgPC9kaXY+CiAgPC9kaXY+CgogIDxzY3JpcHQ+CiAgICBmdW5jdGlvbiBsb2FkRGF0YSgpIHsKICAgICAgZmV0Y2goJy9hcGkvc3RhdHVzJykudGhlbihyID0+IHIuanNvbigpKS50aGVuKGQgPT4gewogICAgICAgIGxldCBhcCA9IGQuYXV0b3BpbG90IHx8IHt9OwogICAgICAgIGxldCBzdGF0dXNIdG1sID0gYFRy4bqhbmcgdGjDoWk6IDxzcGFuIGNsYXNzPSJiYWRnZSAke2FwLmNmZyAmJiBhcC5jZmcuZW5hYmxlZCA/ICdvbicgOiAnb2ZmJ30iPiR7YXAuY2ZnICYmIGFwLmNmZy5lbmFibGVkID8gJ8SQQU5HIENI4bqgWScgOiAnxJDDgyBU4bquVCd9PC9zcGFuPjxicj5gICsKICAgICAgICAgICAgICAgICAgICAgICAgIGBLaG/huqNuZyB0aOG7nWkgZ2lhbjogPGI+JHthcC5jZmcgPyBhcC5jZmcuaW50ZXJ2YWxfbWluIDogMH0gcGjDunQ8L2I+PGJyPmAgKwogICAgICAgICAgICAgICAgICAgICAgICAgYFRp4bq/biB0csOsbmg6IDxiPiR7YXAuYnVzeSA/ICfEkGFuZyB44butIGzDvS4uLicgOiAnU+G6tW4gc8OgbmcnfTwvYj5gOwogICAgICAgIGRvY3VtZW50LmdldEVsZW1lbnRCeUlkKCdzdGF0dXMtYm94JykuaW5uZXJIVE1MID0gc3RhdHVzSHRtbDsKCiAgICAgICAgbGV0IHN0ID0gZC5zdGF0dXMgfHwge307CiAgICAgICAgbGV0IGRpc2sgPSBzdC5kaXNrID8gc3QuZGlzay5odW1hbiA6ICcwR0InOwogICAgICAgIGxldCBzdGF0c0h0bWwgPSBgVOG7lW5nIHPhu5EgdmlkZW8gxJHDoyB04bqhbzogPGI+JHtzdC52aWRlb3MgfHwgMH08L2I+PGJyPmAgKwogICAgICAgICAgICAgICAgICAgICAgICBgxJDDoyB4deG6pXQgYuG6o246IDxiPiR7c3QucHVibGlzaGVkIHx8IDB9PC9iPjxicj5gICsKICAgICAgICAgICAgICAgICAgICAgICAgYER1bmcgbMaw4bujbmcg4buVIGPhu6luZzogPGI+JHtkaXNrfTwvYj5gOwogICAgICAgIGRvY3VtZW50LmdldEVsZW1lbnRCeUlkKCdzdGF0cy1ib3gnKS5pbm5lckhUTUwgPSBzdGF0c0h0bWw7CgogICAgICAgIGlmIChzdC5yZWNlbnQgJiYgQXJyYXkuaXNBcnJheShzdC5yZWNlbnQpKSB7CiAgICAgICAgICBsZXQgdkh0bWwgPSAiPHVsPiI7CiAgICAgICAgICBzdC5yZWNlbnQuZm9yRWFjaCh2ID0+IHsKICAgICAgICAgICAgdkh0bWwgKz0gYDxsaT48Yj4ke3YudGl0bGUgfHwgJ1ZpZGVvJ308L2I+ICgke3YubmljaGUgfHwgJ2dlbmVyYWwnfSkgLSA8aT4ke3YudGltZSB8fCAnJ308L2k+PC9saT5gOwogICAgICAgICAgfSk7CiAgICAgICAgICB2SHRtbCArPSAiPC91bD4iOwogICAgICAgICAgZG9jdW1lbnQuZ2V0RWxlbWVudEJ5SWQoJ3JlY2VudC12aWRlb3MnKS5pbm5lckhUTUwgPSB2SHRtbDsKICAgICAgICB9IGVsc2UgewogICAgICAgICAgZG9jdW1lbnQuZ2V0RWxlbWVudEJ5SWQoJ3JlY2VudC12aWRlb3MnKS5pbm5lckhUTUwgPSAiQ2jGsGEgY8OzIHZpZGVvIGfhuqduIMSRw6J5IG7DoG8uIjsKICAgICAgICB9CiAgICAgIH0pOwoKICAgICAgZmV0Y2goJy9hcGkvY2hhbm5lbHMnKS50aGVuKHIgPT4gci5qc29uKCkpLnRoZW4oZCA9PiB7CiAgICAgICAgbGV0IGxpc3QgPSBkLmNoYW5uZWxzIHx8IFtdOwogICAgICAgIGxldCByb3dzID0gIiI7CiAgICAgICAgbGlzdC5mb3JFYWNoKGMgPT4gewogICAgICAgICAgbGV0IHN0QmFkZ2UgPSBjLmVuYWJsZWQgPyAnPHNwYW4gY2xhc3M9ImJhZGdlIG9uIj5Ib+G6oXQgxJHhu5luZzwvc3Bhbj4nIDogJzxzcGFuIGNsYXNzPSJiYWRnZSBvZmYiPlThuqFtIGThu6tuZzwvc3Bhbj4nOwogICAgICAgICAgcm93cyArPSBgPHRyPjx0ZD48Yj4ke2MubmFtZX08L2I+PGJyPjxzbWFsbCBzdHlsZT0iY29sb3I6IzhiOTQ5ZSI+JHtjLnVybCB8fCBjLmlkfTwvc21hbGw+PC90ZD48dGQ+JHtjLm5pY2hlfTwvdGQ+PHRkPiR7Yy5pbnRlcnZhbF9taW59IHBow7p0PC90ZD48dGQ+JHtzdEJhZGdlfTwvdGQ+PC90cj5gOwogICAgICAgIH0pOwogICAgICAgIGlmKHJvd3MgPT09ICIiKSByb3dzID0gJzx0cj48dGQgY29sc3Bhbj0iNCI+Q2jGsGEgY8OzIGvDqm5oIG7DoG8gxJHGsOG7o2MgY+G6pXUgaMOsbmguPC90ZD48L3RyPic7CiAgICAgICAgZG9jdW1lbnQuZ2V0RWxlbWVudEJ5SWQoJ2NoYW5uZWxzLXRhYmxlJykuaW5uZXJIVE1MID0gcm93czsKICAgICAgfSk7CiAgICB9CgogICAgZnVuY3Rpb24gdG9nZ2xlQXV0byhlbmFibGUpIHsKICAgICAgZmV0Y2goJy9hcGkvYXV0b3BpbG90JywgewogICAgICAgIG1ldGhvZDogJ1BPU1QnLAogICAgICAgIGhlYWRlcnM6IHsnQ29udGVudC1UeXBlJzogJ2FwcGxpY2F0aW9uL2pzb24nfSwKICAgICAgICBib2R5OiBKU09OLnN0cmluZ2lmeSh7ZW5hYmxlZDogZW5hYmxlfSkKICAgICAgfSkudGhlbigoKSA9PiBsb2FkRGF0YSgpKTsKICAgIH0KCiAgICBsb2FkRGF0YSgpOwogICAgc2V0SW50ZXJ2YWwobG9hZERhdGEsIDUwMDApOwogIDwvc2NyaXB0Pgo8L2JvZHk+CjwvaHRtbD4K").decode("utf-8")
if HAVE_FASTAPI:
    @app.get("/api/status")
    def api_status():
        return JSONResponse(status())
    @app.get("/api/videos")
    def api_videos():
        return JSONResponse(videos())
    @app.get("/api/channels")
    def api_channels():
        return JSONResponse(channels_list())
    @app.get("/api/channel")
    def api_channel():
        return JSONResponse(channel_real())


    @app.get("/api/analytics")
    def api_analytics():
        return JSONResponse(analytics())

    @app.get("/api/content")
    def api_content():
        return JSONResponse(content_db())

    @app.get("/api/activity")
    def api_activity():
        return JSONResponse(activity())

    @app.post("/api/delete")
    def api_delete(payload: dict):
        return JSONResponse(delete_video(payload.get("path", "")))
    @app.post("/api/automation")
    def api_automation(payload: dict):
        return JSONResponse(set_automation(payload.get("flag"), payload.get("value")))
    @app.post("/api/cleanup")
    def api_cleanup():
        return JSONResponse({"ok": True, "removed": cleanup_junk()})
    @app.post("/api/run")
    def api_run(payload: dict):
        return JSONResponse(run_script(payload.get("script", ""), payload.get("args")))
    @app.post("/api/published")
    def api_published(payload: dict):
        return JSONResponse(add_published(payload.get("youtube_id"), payload.get("topic"), payload.get("score")))
    @app.get("/api/trend")
    def api_trend():
        import trend as TR
        TR.snapshot()
        return JSONResponse(TR.trend())
    @app.get("/api/top")
    def api_top():
        import trend as TR
        return JSONResponse(TR.top(5))
    @app.get("/api/brief")
    def api_brief():
        import trend as TR
        TR.snapshot()
        return JSONResponse(TR.brief())
    @app.get("/api/manager")
    def api_manager():
        import video_manager as VM
        return JSONResponse(VM.summary())

    @app.get("/api/tools")
    def api_tools():
        import tool_registry as TR
        import json as j
        try: return JSONResponse(j.load(open(TR.OUT,encoding="utf-8")))
        except: return JSONResponse(TR.build())
    try:
        from ops import os_api as _OA
        _OA.add_routes(app)
    except Exception:
        pass
    @app.get("/", response_class=HTMLResponse)
    def index():
        try:
            return open(os.path.join(ROOT, "dashboard.html"), encoding="utf-8").read()
        except Exception:
            return HTML
@app.post("/api/batch-publish")
def trigger_batch_publish():
    from ops.batch_pipeline import run_batch
    import threading
    threading.Thread(target=run_batch, daemon=True).start()
    return {"status": "success", "message": "Tiến trình batch đang chạy ngầm"}


@app.post("/api/batch-publish")
def trigger_batch_publish():
    from ops.batch_pipeline import run_batch
    import threading
    threading.Thread(target=run_batch, daemon=True).start()
    return {"status": "success", "message": "Batch publishing started in background"}


def main():
    print(json.dumps(status(), indent=2))
    if HAVE_FASTAPI:
        start_worker()
        import uvicorn, threading, webbrowser
        port = int(os.environ.get("DASH_PORT", 8787))
        threading.Timer(2.0, lambda: webbrowser.open(f"http://localhost:{port}")).start()
        uvicorn.run(app, host="0.0.0.0", port=port)
if __name__ == "__main__":
    main()
