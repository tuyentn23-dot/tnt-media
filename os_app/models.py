"""TNT Media OS - models."""
import json
from dataclasses import dataclass, field
from typing import Optional
from . import db

@dataclass
class Cycle:
    id: Optional[int] = None
    started_at: str = ""
    ended_at: Optional[str] = None
    stage: str = "plan"
    goal: Optional[str] = None
    status: str = "running"
    meta: dict = field(default_factory=dict)

@dataclass
class Video:
    id: Optional[int] = None
    cycle_id: Optional[int] = None
    path: Optional[str] = None
    youtube_id: Optional[str] = None
    title: Optional[str] = None
    topic: Optional[str] = None
    format: Optional[str] = None
    score: Optional[float] = None
    status: str = "created"
    published_at: Optional[str] = None
    created_at: str = ""
    meta: dict = field(default_factory=dict)

@dataclass
class Metric:
    id: Optional[int] = None
    video_id: int = 0
    ts: str = ""
    views: int = 0
    ctr: Optional[float] = None
    retention: Optional[float] = None
    likes: int = 0
    comments: int = 0
    source: str = "youtube"
    raw: dict = field(default_factory=dict)

@dataclass
class Insight:
    id: Optional[int] = None
    cycle_id: Optional[int] = None
    kind: str = "general"
    finding: str = ""
    evidence: dict = field(default_factory=dict)
    created_at: str = ""

@dataclass
class Decision:
    id: Optional[int] = None
    cycle_id: Optional[int] = None
    rule_key: str = ""
    old_value: Optional[str] = None
    new_value: Optional[str] = None
    reason: Optional[str] = None
    applied_at: Optional[str] = None
    result: dict = field(default_factory=dict)

def _d(row):
    return {k: row[k] for k in row.keys()}

def create_cycle(goal=None, stage="plan"):
    with db.tx() as conn:
        cur = conn.execute("INSERT INTO cycles(started_at, stage, goal, status) VALUES(?,?,?,?)", (db.now(), stage, goal, "running"))
        return cur.lastrowid

def update_cycle(cid, **fields):
    if not fields:
        return
    keys = ", ".join(k + "=?" for k in fields)
    with db.tx() as conn:
        conn.execute("UPDATE cycles SET " + keys + " WHERE id=?", list(fields.values()) + [cid])

def get_cycle(cid):
    with db.tx() as conn:
        r = conn.execute("SELECT * FROM cycles WHERE id=?", (cid,)).fetchone()
        return _d(r) if r else None

def latest_cycle():
    with db.tx() as conn:
        r = conn.execute("SELECT * FROM cycles ORDER BY id DESC LIMIT 1").fetchone()
        return _d(r) if r else None

def list_cycles(limit=50):
    with db.tx() as conn:
        rows = conn.execute("SELECT * FROM cycles ORDER BY id DESC LIMIT ?", (limit,)).fetchall()
        return [_d(r) for r in rows]

def add_video(v):
    if not v.created_at:
        v.created_at = db.now()
    with db.tx() as conn:
        cur = conn.execute("INSERT INTO videos(cycle_id,path,youtube_id,title,topic,format,score,status,published_at,created_at,meta_json) VALUES(?,?,?,?,?,?,?,?,?,?,?)",
            (v.cycle_id, v.path, v.youtube_id, v.title, v.topic, v.format, v.score, v.status, v.published_at, v.created_at, json.dumps(v.meta, ensure_ascii=False)))
        return cur.lastrowid

def list_videos(limit=100, cycle_id=None):
    with db.tx() as conn:
        if cycle_id is None:
            rows = conn.execute("SELECT * FROM videos ORDER BY id DESC LIMIT ?", (limit,)).fetchall()
        else:
            rows = conn.execute("SELECT * FROM videos WHERE cycle_id=? ORDER BY id DESC LIMIT ?", (cycle_id, limit)).fetchall()
        return [_d(r) for r in rows]

def get_video(vid):
    with db.tx() as conn:
        r = conn.execute("SELECT * FROM videos WHERE id=?", (vid,)).fetchone()
        return _d(r) if r else None

def update_video(vid, **fields):
    if not fields:
        return
    keys = ", ".join(k + "=?" for k in fields)
    with db.tx() as conn:
        conn.execute("UPDATE videos SET " + keys + " WHERE id=?", list(fields.values()) + [vid])

def add_metric(m):
    if not m.ts:
        m.ts = db.now()
    with db.tx() as conn:
        cur = conn.execute("INSERT INTO metrics(video_id,ts,views,ctr,retention,likes,comments,source,raw_json) VALUES(?,?,?,?,?,?,?,?,?)",
            (m.video_id, m.ts, m.views, m.ctr, m.retention, m.likes, m.comments, m.source, json.dumps(m.raw, ensure_ascii=False)))
        return cur.lastrowid

def latest_metric(video_id):
    with db.tx() as conn:
        r = conn.execute("SELECT * FROM metrics WHERE video_id=? ORDER BY ts DESC LIMIT 1", (video_id,)).fetchone()
        return _d(r) if r else None

def list_metrics(limit=200):
    with db.tx() as conn:
        rows = conn.execute("SELECT * FROM metrics ORDER BY ts DESC LIMIT ?", (limit,)).fetchall()
        return [_d(r) for r in rows]

def add_insight(i):
    if not i.created_at:
        i.created_at = db.now()
    with db.tx() as conn:
        cur = conn.execute("INSERT INTO insights(cycle_id,kind,finding,evidence_json,created_at) VALUES(?,?,?,?,?)",
            (i.cycle_id, i.kind, i.finding, json.dumps(i.evidence, ensure_ascii=False), i.created_at))
        return cur.lastrowid

def list_insights(limit=50):
    with db.tx() as conn:
        rows = conn.execute("SELECT * FROM insights ORDER BY id DESC LIMIT ?", (limit,)).fetchall()
        return [_d(r) for r in rows]

def add_decision(d):
    if not d.applied_at:
        d.applied_at = db.now()
    with db.tx() as conn:
        cur = conn.execute("INSERT INTO decisions(cycle_id,rule_key,old_value,new_value,reason,applied_at,result_json) VALUES(?,?,?,?,?,?,?)",
            (d.cycle_id, d.rule_key, d.old_value, d.new_value, d.reason, d.applied_at, json.dumps(d.result, ensure_ascii=False)))
        return cur.lastrowid

def list_decisions(limit=50):
    with db.tx() as conn:
        rows = conn.execute("SELECT * FROM decisions ORDER BY id DESC LIMIT ?", (limit,)).fetchall()
        return [_d(r) for r in rows]

def log_tool_run(cycle_id, tool, args, ok, ms, output):
    with db.tx() as conn:
        cur = conn.execute("INSERT INTO tool_runs(cycle_id,tool,args_json,ok,ms,output,ran_at) VALUES(?,?,?,?,?,?,?)",
            (cycle_id, tool, json.dumps(args, ensure_ascii=False), 1 if ok else 0, ms, (output or "")[:8000], db.now()))
        return cur.lastrowid

def list_tool_runs(limit=100):
    with db.tx() as conn:
        rows = conn.execute("SELECT * FROM tool_runs ORDER BY id DESC LIMIT ?", (limit,)).fetchall()
        return [_d(r) for r in rows]

def dashboard_summary():
    with db.tx() as conn:
        counts = {}
        for t in ["cycles","videos","metrics","insights","decisions","experiments","tool_runs"]:
            counts[t] = conn.execute("SELECT COUNT(*) AS n FROM " + t).fetchone()["n"]
        latest = conn.execute("SELECT * FROM cycles ORDER BY id DESC LIMIT 1").fetchone()
        vids = conn.execute("SELECT id,title,topic,youtube_id,score,status,published_at,created_at FROM videos ORDER BY id DESC LIMIT 10").fetchall()
        ins = conn.execute("SELECT * FROM insights ORDER BY id DESC LIMIT 10").fetchall()
        dec = conn.execute("SELECT * FROM decisions ORDER BY id DESC LIMIT 10").fetchall()
    return {"counts": counts, "latest_cycle": _d(latest) if latest else None, "videos": [_d(r) for r in vids], "insights": [_d(r) for r in ins], "decisions": [_d(r) for r in dec]}


@dataclass
class Experiment:
    id: Optional[int] = None
    name: str = ""
    variant_a: str = ""
    variant_b: str = ""
    metric: str = ""
    winner: Optional[str] = None
    started_at: str = ""
    ended_at: Optional[str] = None

def add_experiment(e):
    if not e.started_at:
        e.started_at = db.now()
    with db.tx() as conn:
        cur = conn.execute("INSERT INTO experiments(name,variant_a,variant_b,metric,winner,started_at,ended_at) VALUES(?,?,?,?,?,?,?)",
            (e.name, e.variant_a, e.variant_b, e.metric, e.winner, e.started_at, e.ended_at))
        return cur.lastrowid

def list_experiments(limit=50):
    with db.tx() as conn:
        rows = conn.execute("SELECT * FROM experiments ORDER BY id DESC LIMIT ?", (limit,)).fetchall()
        return [_d(r) for r in rows]

def update_experiment(eid, **fields):
    if not fields:
        return
    keys = ", ".join(k + "=?" for k in fields)
    with db.tx() as conn:
        conn.execute("UPDATE experiments SET " + keys + " WHERE id=?", list(fields.values()) + [eid])
