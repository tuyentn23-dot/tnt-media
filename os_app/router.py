"""TNT Media OS - FastAPI router mounted at /os."""
import json
import os
from pathlib import Path
from fastapi import APIRouter
from fastapi.responses import HTMLResponse, JSONResponse
from . import db
from . import models as M

HERE = Path(os.path.dirname(os.path.abspath(__file__)))
UI_DIR = HERE / "ui"
PKG_ROOT = HERE.parent
router = APIRouter(prefix="/os", tags=["os"])

def _serve(name):
    p = UI_DIR / name
    if not p.exists():
        return HTMLResponse("<h1>UI missing: " + name + "</h1>", status_code=404)
    return HTMLResponse(p.read_text(encoding="utf-8"))

def _boot():
    try:
        db.init()
    except Exception:
        pass

@router.get("", response_class=HTMLResponse)
@router.get("/", response_class=HTMLResponse)
def index():
    _boot()
    return _serve("index.html")

@router.get("/health")
def health():
    _boot()
    return JSONResponse(db.health())

@router.get("/api/summary")
def summary():
    _boot()
    return JSONResponse(M.dashboard_summary())

@router.get("/api/charts")
def charts():
    _boot()
    try:
        c = db.connect()
        by_topic = c.execute('SELECT topic, COUNT(1) n FROM videos WHERE topic IS NOT NULL GROUP BY topic ORDER BY n DESC LIMIT 12').fetchall()
        by_day = c.execute('SELECT substr(published_at,1,10) d, COUNT(1) n FROM videos WHERE youtube_id IS NOT NULL AND published_at IS NOT NULL GROUP BY d ORDER BY d DESC LIMIT 14').fetchall()
        scores = c.execute('SELECT score FROM videos WHERE score IS NOT NULL ORDER BY id DESC LIMIT 20').fetchall()
        return JSONResponse(dict(ok=True, by_topic=[[r[0], r[1]] for r in by_topic], by_day=[[r[0], r[1]] for r in reversed(by_day)], scores=[r[0] for r in reversed(scores)]))
    except Exception as e:
        return JSONResponse(dict(ok=False, error=str(e)))

@router.get("/api/cycles")
def cycles(limit: int = 50):
    return JSONResponse({"items": M.list_cycles(limit)})

@router.post("/api/cycles")
def new_cycle(goal: str = None, stage: str = "plan"):
    cid = M.create_cycle(goal=goal, stage=stage)
    return JSONResponse({"id": cid})

@router.get("/api/videos")
def videos(limit: int = 100, cycle_id: int = None):
    return JSONResponse({"items": M.list_videos(limit, cycle_id)})

@router.get("/api/metrics")
def metrics(limit: int = 200):
    return JSONResponse({"items": M.list_metrics(limit)})

@router.get("/api/insights")
def insights(limit: int = 50):
    return JSONResponse({"items": M.list_insights(limit)})

@router.get("/api/decisions")
def decisions(limit: int = 50):
    return JSONResponse({"items": M.list_decisions(limit)})

@router.get("/api/tool_runs")
def tool_runs(limit: int = 100):
    return JSONResponse({"items": M.list_tool_runs(limit)})

@router.get("/api/tools")
def tools():
    p = PKG_ROOT / "memory" / "tool_registry.json"
    if p.exists():
        try:
            return JSONResponse(json.loads(p.read_text(encoding="utf-8")))
        except Exception as e:
            return JSONResponse({"error": str(e), "tools": []})
    return JSONResponse({"tools": []})

@router.get("/api/settings")
def settings():
    return JSONResponse({
        "youtube_token": (PKG_ROOT / "memory" / "token.json").exists(),
        "client_secrets": (PKG_ROOT / "config" / "client_secrets.json").exists(),
        "db": str(db.DB_PATH),
        "env": {"PEXELS_API_KEY": bool(os.environ.get("PEXELS_API_KEY")), "YOUTUBE_API_KEY": bool(os.environ.get("YOUTUBE_API_KEY"))}
    })

@router.post("/api/run_cycle")
def run_cycle(goal: str = None):
    from .engine import orchestrator as ORCH
    log = ORCH.run_once(goal=goal)
    return JSONResponse(log)

@router.post("/api/check/ingest")
def ingest(limit: int = 10):
    from .engine import check as CHECK
    return JSONResponse(CHECK.run(None, limit=limit))

@router.post("/api/do/run")
def do_run(tool: str, cycle_id: int = None):
    from .adapters import tool_adapter as TA
    return JSONResponse(TA.run_tool(tool, [], cycle_id=cycle_id))

@router.get("/api/scheduler")
def scheduler_status():
    from .engine import scheduler as S
    return JSONResponse(S.status())

@router.post("/api/scheduler/start")
def scheduler_start(interval_sec: int = 3600):
    from .engine import scheduler as S
    return JSONResponse(S.start(interval_sec))

@router.post("/api/scheduler/stop")
def scheduler_stop():
    from .engine import scheduler as S
    return JSONResponse(S.stop())

@router.post("/api/publish")
def publish(path: str, title: str, topic: str = "", cycle_id: int = None):
    import importlib.util
    from pathlib import Path
    spec = importlib.util.spec_from_file_location("osp", str(Path(os.getcwd()) / "ops" / "os_publish.py"))
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return JSONResponse(m.publish(path, title, topic=topic, cycle_id=cycle_id))


@router.post("/api/quality/check")
def quality_check(path: str):
    from ops.quality_gate import evaluate
    return JSONResponse(evaluate(path))

@router.get("/api/quality/ranking")
def quality_ranking(limit: int = 20):
    from ops.video_quality import rank_footage
    import glob
    paths = sorted(glob.glob(os.path.join(os.getcwd(), "library", "*", "*.mp4")))[:limit]
    ranked = rank_footage(paths)
    return JSONResponse({"items": [p.replace(os.getcwd(), "") for p in ranked]})

@router.post("/api/build")
def build(paths: str = '', hook: str = '', target_dur: float = 12.0, out: str = '', voice: str = '', music: str = '', topic: str = ''):
    from ops.video_quality import build_short
    import json as _j, time
    from ops import content_planner as _cp
    if not paths:
        return JSONResponse(dict(ok=False, error='paths required'))
    try:
        plist = _j.loads(paths)
    except Exception:
        plist = [x.strip() for x in paths.split(',') if x.strip()]
    hook_text = hook
    script = []
    if topic and (not hook_text or not script):
        h2, l2, _ = _cp.for_topic(topic)
        if not hook_text:
            hook_text = h2
        script = l2
    voice_text = voice or (' '.join(script) if script else None)
    mus = music or None
    if not out:
        ts = time.strftime('%Y%m%d_%H%M%S')
        out = 'output/ui_' + (topic or 'build') + '_' + ts + '.mp4'
    try:
        build_short(plist, script, out, hook_text=hook_text or None, music_path=mus, target_dur=float(target_dur), voice_text=voice_text)
        from ops.quality_gate import evaluate
        return JSONResponse(dict(ok=True, out=out, quality=evaluate(out)))
    except Exception as e:
        return JSONResponse(dict(ok=False, error=str(e)))

@router.post("/api/autopublish")
def autopublish(topic: str = '', target_dur: float = 14.0, dry: bool = False):
    from ops.auto_publish import run
    try:
        r = run(topic or None, target_dur=float(target_dur), force=dry)
        return JSONResponse(r)
    except Exception as e:
        return JSONResponse(dict(ok=False, error=str(e)))

@router.get("/api/experiments")
def experiments(limit: int = 50):
    return JSONResponse({"items": M.list_experiments(limit)})

@router.post("/api/experiments")
def create_experiment(name: str, variant_a: str = "", variant_b: str = "", metric: str = "viral_score"):
    eid = M.add_experiment(M.Experiment(name=name, variant_a=variant_a, variant_b=variant_b, metric=metric))
    return JSONResponse({"ok": True, "id": eid})

@router.post("/api/experiments/decide")
def decide_experiment(eid: int, winner: str):
    M.update_experiment(eid, winner=winner, ended_at=db.now())
    M.add_insight(M.Insight(cycle_id=None, kind="experiment_result", finding="Experiment "+str(eid)+" winner="+winner, evidence={"eid": eid, "winner": winner}))
    return JSONResponse({"ok": True})

@router.post("/api/auto_publish")
def auto_publish(topic: str, hook: str = "", title: str = "", target_dur: float = 12.0, force: bool = False):
    from ops.auto_publish import run as _auto
    try:
        res = _auto(topic, hook_text=hook or None, title=title or None, target_dur=float(target_dur), force=force)
        return JSONResponse(res)
    except Exception as e:
        return JSONResponse({"ok": False, "error": str(e)})

@router.get("/api/channels")
def channels_list():
	from ops import channel_loader as ch
	from ops import content_freshness as cf
	out = []
	for cid in ch.list_channels():
		try:
			cfg = ch.load(cid)
		except Exception as e:
			out.append({"id": cid, "error": str(e)}); continue
		cf.set_channel(cid)
		kinds = cfg.get("content", {}).get("kinds", [])
		fresh = {}
		for k in kinds:
			items = ch.load_content(cid, k)
			fresh[k] = len([it for it in items if not cf.is_published(cf.signature(it, k))])
		out.append({"id": cid, "name": cfg.get("name"), "enabled": cfg.get("enabled"), "kinds": kinds, "fresh": fresh, "schedule": cfg.get("schedule", {}), "published": cf.published_count()})
	return JSONResponse({"items": out})

@router.post("/api/channels/{cid}/toggle")
def channel_toggle(cid: str, enabled: bool = True):
	from ops import channel_loader as ch
	cfg = ch.load(cid)
	cfg["enabled"] = bool(enabled)
	ch.save(cid, cfg)
	return JSONResponse({"ok": True, "id": cid, "enabled": enabled})

@router.get("/api/channels/{cid}/content")
def channel_content(cid: str, kind: str = None):
	from ops import channel_loader as ch
	from ops import content_freshness as cf
	cf.set_channel(cid)
	items = ch.load_content(cid, kind) if kind else ch.load_content(cid)
	if kind:
		rows = []
		for it in items:
			sig = cf.signature(it, kind)
			rows.append({"id": it.get("id"), "hook": it.get("hook"), "published": cf.is_published(sig)})
		return JSONResponse({"items": rows})
	return JSONResponse({"items": items})

@router.post("/api/multichannel/run")
def multichannel_run(per_channel: int = 2):
    from ops.multichannel_runner import run_all
    try:
        return JSONResponse({"items": run_all(per_channel=per_channel)})
    except Exception as e:
        return JSONResponse({"ok": False, "error": str(e)[:200]})


@router.get("/api/multichannel/state")
def multichannel_state():
    import json, os
    p = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'memory', 'multichannel_state.json')
    if os.path.exists(p):
        try:
            return JSONResponse(json.loads(open(p, encoding='utf-8').read()))
        except Exception as e:
            return JSONResponse({"error": str(e)})
    return JSONResponse({"cycle": 0, "last_run": {}})


@router.get("/api/video/health")
def video_health_api(path: str):
    from ops.video_health import check
    return JSONResponse(check(path))

@router.get("/api/gallery")
def gallery(limit: int = 60):
    import os, glob, time
    out = []
    d = os.path.join(PKG_ROOT, 'output')
    if os.path.isdir(d):
        files = sorted(glob.glob(os.path.join(d, '*.mp4')), key=lambda p: os.path.getmtime(p), reverse=True)
        for p in files[:limit]:
            try:
                sz = os.path.getsize(p)
            except Exception:
                sz = 0
            out.append({'name': os.path.basename(p), 'size': sz, 'mtime': os.path.getmtime(p), 'url': '/os/file/' + os.path.basename(p)})
    return JSONResponse({'items': out})


@router.get("/file/{name}")
def serve_file(name: str):
    import os
    from fastapi.responses import FileResponse
    p = os.path.join(PKG_ROOT, 'output', os.path.basename(name))
    if not os.path.exists(p):
        return JSONResponse({'ok': False, 'error': 'not found'}, status_code=404)
    return FileResponse(p, media_type='video/mp4')

@router.post("/api/agent/open_url")
def agent_open_url(url: str):
    from ops import agent_tools as at
    return JSONResponse(at.open_url(url))


@router.post("/api/agent/screenshot")
def agent_screenshot():
    from ops import agent_tools as at
    return JSONResponse(at.screenshot())


@router.get("/api/agent/actions")
def agent_actions(limit: int = 50):
    from ops import agent_tools as at
    return JSONResponse({"items": at.list_actions(limit)})


@router.post("/api/agent/run_cmd")
def agent_run_cmd(cmd: str, timeout: int = 30):
    from ops import agent_tools as at
    return JSONResponse(at.run_cmd(cmd, timeout=timeout))


@router.post("/api/agent/read_screen")
def agent_read_screen():
    from ops import agent_tools as at
    return JSONResponse(at.read_screen_text())

@router.post("/api/channels/{cid}/publish")
def channel_publish(cid: str, count: int = 2):
    from ops.multichannel_runner import publish_one_channel
    try:
        return JSONResponse(publish_one_channel(cid, per_channel=count))
    except Exception as e:
        return JSONResponse({"ok": False, "error": str(e)[:200]})


@router.get("/control", response_class=HTMLResponse)
def control_page():
    return _serve("control.html")


@router.get('/api/state')
def state_api(limit: int = 20):
    import sqlite3
    p = PKG_ROOT / 'system' / 'state.db'
    if not p.exists():
        return {'ok': False, 'error': 'state.db not found'}
    c = sqlite3.connect(str(p))
    c.row_factory = sqlite3.Row
    def rows(s, a=()):
        return [dict(x) for x in c.execute(s, a).fetchall()]
    out = {}
    out['trends'] = rows('SELECT id, topic, score, snapshotAt FROM trends ORDER BY id DESC LIMIT ?', (limit,))
    out['decisions'] = rows('SELECT id, channelId, topic, format, hook, score, rationale, chosenAt FROM decisions ORDER BY id DESC LIMIT ?', (limit,))
    out['publishes'] = rows('SELECT videoId, url, publishedAt, status FROM publishes ORDER BY id DESC LIMIT ?', (limit,))
    out['counts'] = dict(trends=rows('SELECT COUNT(1) c FROM trends')[0]['c'], decisions=rows('SELECT COUNT(1) c FROM decisions')[0]['c'], publishes=rows('SELECT COUNT(1) c FROM publishes')[0]['c'])
    c.close()
    return out
