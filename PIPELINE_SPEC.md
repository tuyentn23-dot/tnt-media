# PIPELINE SPEC - TNT Media

> Version 1.0 - Phase 0 - Frozen schema
> Trang thai: DRAFT -> REVIEW -> FROZEN
> Moi thay doi schema phai bump version + ghi CHANGELOG

---

## 1. Muc tieu

Thay the cac phien lam viec roi rac bang MOT pipeline cung, quan ly boi mini app.
Chat/agent chi nang cap tung module, KHONG tu dang video, KHONG sua pipeline.

## 2. Ba mat phang (Planes)

| Plane | Ai dung | Duoc sua? | Giao tiep qua |
|---|---|---|---|
| Control (Mini App) | Nguoi | Co (qua UI) | HTTP API -> DB |
| Data (Pipeline) | May | KHONG | API noi bo + DB |
| Dev (Chat/Agent) | Nguoi + Agent | Chi modules/ | Doc spec + DB |

Nguyen tac vang:
- Control plane KHONG BAO GIO goi truc tiep module
- Data plane KHONG BAO GIO tu quyet dinh
- Dev plane KHONG BAO GIO tu dang

## 3. Kien truc tong the


CONTROL PLANE
 Tray -> Web UI (localhost:7777) -> API (FastAPI) -> DB
 |
DATA PLANE v
 queue -> worker -> modules/* -> publish -> SQLite
 ^
DEV PLANE |
 Chat/Agent -> chi sua modules/*.py ---------+


---

## 4. Database Schema (SQLite)

File: state/pipeline.db - NGUON SU THAT DUY NHAT

### 4.1 Bang channels
sql
CREATE TABLE channels (
 id TEXT PRIMARY KEY, -- Mialinhcute, vilevi5676
 enabled INTEGER DEFAULT 1,
 niche TEXT, -- JSON array
 forbidden TEXT, -- JSON array
 kinds TEXT, -- JSON array, thu tu uu tien
 voice TEXT, -- JSON {engine,name,rate}
 max_length_sec INTEGER DEFAULT 60,
 style TEXT, -- JSON
 schedule TEXT, -- JSON {slots,per_day}
 publish_mode TEXT DEFAULT "approve", -- auto|approve
 quality_gate TEXT DEFAULT "normal",
 created_at TEXT, updated_at TEXT
);


### 4.2 Bang jobs
sql
CREATE TABLE jobs (
 id TEXT PRIMARY KEY,
 channel_id TEXT NOT NULL,
 topic TEXT,
 kind TEXT,
 length_override INTEGER,
 voice_override TEXT,
 music_mood TEXT,
 count INTEGER DEFAULT 1,
 require_approval INTEGER DEFAULT 1,
 run_at TEXT,
 repeat TEXT, -- cron hoac null
 status TEXT DEFAULT "pending", -- pending|running|done|failed|cancelled
 priority INTEGER DEFAULT 5,
 created_by TEXT, -- user|agent|scheduler
 created_at TEXT, updated_at TEXT,
 error TEXT
);


### 4.3 Bang publications
sql
CREATE TABLE publications (
 id INTEGER PRIMARY KEY AUTOINCREMENT,
 job_id TEXT,
 channel_id TEXT,
 signature TEXT UNIQUE, -- chong trung
 topic TEXT, kind TEXT,
 title TEXT, youtube_id TEXT,
 file_path TEXT, -- duong dan local
 status TEXT, -- rendered|pending_approval|published|failed
 view_count INTEGER DEFAULT 0,
 like_count INTEGER DEFAULT 0,
 quota_cost INTEGER DEFAULT 0,
 published_at TEXT, created_at TEXT
);


### 4.4 Cac bang khac
- topics - pool + cooldown
- assets - music/footage/voice presets
- audit - ai sua gi, khi nao
- quota - YouTube quota con lai per account per day
- modules_ver - version tung module, ho tro rollback
- trends - trend history + feedback loop

## 5. Module Contract

Moi module trong modules/ PHAI khai bao:

python
MODULE = {
 "name": "voice_engine",
 "version": "2.0.0",
 "interface": "run(job: Job, ctx: Ctx) -> Result",
 "config_schema": {...},
 "deps": ["edge-tts>=6.1"],
 "health": "health() -> bool"
}


Pipeline TU CHOI module sai interface. Agent sua module PHAI bump version.

---

## 6. API Contract (FastAPI, localhost:7777)

### 6.1 Read-only (Phase 2)
| Method | Path | Mo ta |
|---|---|---|
| GET | /api/health | Trang thai he thong |
| GET | /api/channels | Danh sach kenh |
| GET | /api/channels/{id} | Chi tiet kenh |
| GET | /api/jobs | Danh sach job |
| GET | /api/publications | Video da dang |
| GET | /api/quota | YouTube quota con lai |
| GET | /api/trends | Trend hien tai |
| GET | /api/assets | Music/footage |

### 6.2 Write (Phase 4)
| Method | Path | Mo ta |
|---|---|---|
| POST | /api/jobs | Tao job moi |
| PUT | /api/jobs/{id} | Sua job |
| DELETE | /api/jobs/{id} | Huy job |
| POST | /api/jobs/{id}/approve | Duyet dang |
| POST | /api/jobs/{id}/reject | Tu choi |
| POST | /api/jobs/{id}/retry | Chay lai |
| PUT | /api/channels/{id} | Sua kenh |
| POST | /api/cleanup | Xoa video da dang |
| POST | /api/killswitch | Dung khan cap |

### 6.3 Headless CLI (cho agent)
bash
python -m pipeline.runner --job-json '{"channel":"Mialinhcute",...}'
python -m pipeline.selfcheck
python -m pipeline.migrate
python -m pipeline.cleanup --force


## 7. Approval Workflow (P0)


Job -> render -> status=pending_approval
 |
 [Neu publish_mode=auto] -> publish ngay
 [Neu publish_mode=approve] -> cho UI duyet
 |
 UI: [Approve] -> publish
 [Reject] -> xoa + ghi ly do


Default: publish_mode=approve. Nut gat trong UI de doi.

## 8. Co che Tu Tien Hoa (Self-evolution)

### 8.1 Vong phan hoi

publish -> thu thap view/like/comment (sau 24h, 72h, 7 ngay)
 -> cap nhat bang trends + publications
 -> trend_engine boost topic view cao
 -> topic_picker uu tien topic do
 -> job moi -> publish -> ...


### 8.2 Trend ingestion
- Nguon: YouTube trending, Google Trends, social listening
- Chay moi 6h -> bang trends
- Trend score = f(view_trend, velocity, niche_match)

### 8.3 A/B testing tu dong
- Moi topic render 2 bien the (hook A vs hook B)
- Dang xen ke, so sanh sau 24h
- Winner -> template cho topic tuong tu

### 8.4 Module self-upgrade (Phase 6)
- Moi module co the chay benchmark() -> diem
- Neu version moi < version cu -> rollback tu dong
- Ghi ket qua vao audit

### 8.5 Quota-aware scheduling
- Doc quota con lai -> tinh so video co the dang
- Neu quota < nguong -> giam tan suat, uu tien topic tot nhat
- Reset quota moi ngay 00:00 PT (gio YouTube)

---

## 9. Roadmap Migration (6 phase, khong downtime)

| Phase | Viec | Rui ro | Trang thai |
|---|---|---|---|
| 0 | Spec + AGENT_RULES + DB schema | 0 | DANG LAM |
| 1 | Tao pipeline.db, migrate 4 ledger | 0 | Cho |
| 2 | pipeline/runner.py + API read-only | 0 | Cho |
| 3 | Web UI: Dashboard + Channels + Publications | 0 | Cho |
| 4 | Job Builder + Queue + API write | Trung | Cho |
| 5 | Approval + Analytics + Assets + Settings | 0 | Cho |
| 6 | Tray integration, tat duong publish cu | Cao | Cho |

## 10. Cau truc thu muc dich


media/
 app/ # Mini app
 tray.py # Tray menu
 server.py # FastAPI
 ui/ # HTML + Alpine.js + Tailwind
 defaults.py # Default tu trend
 pipeline/ # HARD, cam sua
 runner.py # Orchestrator
 job.py # Job dataclass
 scheduler.py # APScheduler
 state.py # SQLite API
 selfcheck.py # Health check
 migrate.py # Migration tool
 modules/ # AGENT LAM VIEC O DAY
 content/ # loader, freshness, trend
 render/ # video, music, beat_sync
 voice/ # TTS engines
 publish/ # YouTube wrapper
 config/
 channels.yaml # Import/export
 jobs.yaml # Job templates
 state/
 pipeline.db # NGUON SU THAT
 backup/ # Backup moi gio
 PIPELINE_SPEC.md # File nay
 AGENT_RULES.md # Quy tac cho agent
 STATE.md # Auto-generated tu DB


## 11. UI Plan (Mini App)

Tab chinh:
1. Dashboard - health, quota, trend, loi gan day
2. Channels - CRUD + import/export YAML
3. Jobs - builder + queue + scheduler
4. Publications - bang video da dang + cleanup
5. Topics - pool + cooldown + idea expander
6. Assets - music/footage/voice
7. Analytics - view/like, top/worst, A/B
8. Diagnostics - test render, logs, selfcheck
9. Settings - credentials, killswitch, audit log

Tech: FastAPI + SQLModel + HTML/Alpine.js/Tailwind CDN.
Khong can build. Sua 1 file -> refresh thay ngay.

## 12. Tieu chi nghiem thu

- [ ] Khong con file ledger rai rac (chi con pipeline.db)
- [ ] Khong the dang video ma khong qua pipeline
- [ ] Agent sua module khong the lam hong pipeline
- [ ] Co the rollback module ve version truoc
- [ ] Quota YouTube hien thi realtime
- [ ] Approval workflow hoat dong
- [ ] Audit log ghi moi thay doi
- [ ] Self-evolution loop chay (trend -> job -> publish -> feedback)
- [ ] Backup DB tu dong moi gio
- [ ] Selfcheck PASS truoc moi commit

---

## 13. Quyet dinh da chot

- UI: nhe (HTML + Alpine.js)
- Approval: CO, nut gat, default bat
- YouTube: ca 1-1 va 1-nhieu deu ho tro
- Agent: duoc tao job, KHONG duoc approve/dang
- Self-evolution: CO (Section 8)

## 14. Lien ket

- AGENT_RULES.md - Quy tac cho moi phien
- PHIEN_HANDOFF.md - Handoff phien truoc
- CHANGELOG.md - Lich su thay doi

