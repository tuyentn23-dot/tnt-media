# TNT Media OS - PDCA Closed-Loop Engine

Vong PDCA khep kin: phan tich -> tao -> dang -> tong hop phan hoi -> phan tich -> cap nhat -> tien hoa.
Mo tai: http://localhost:8787/os (canh Control Center cu).

## Trang thai: P0-P4 XONG, P5 ready

## Kien truc

:8787 ops/control_center.py (FastAPI)
 +-- /os -> os_app/router.py (16 routes)
 +-- db.py SQLite: memory/tnt_media.db
 +-- models.py Cycle/Video/Metric/Insight/Decision + DAO
 +-- schema.sql DDL (7 bang)
 +-- engine/
 | +-- plan.py, do.py, check.py, act.py
 | +-- orchestrator.py (run_once)
 | +-- scheduler.py (24/7 background)
 +-- adapters/
 | +-- tool_adapter.py (boc 117 tool ops/)
 | +-- youtube_metrics.py (live YouTube API)
 +-- ui/index.html (SPA 7 tab, ~8KB)
 +-- _migrate.py (published.json -> DB)


## Da verify that
- DB: 7 bang khoi tao OK
- Migration: 21 records tu published.json
- Adapter: chay quality_standard.py -> log tool_run
- YouTube API: channel ViLe Vi (6.07M views, 7320 subs, 892 videos)
- PDCA cycle: chay 4 stage end-to-end (cycle 6)
- Check: sinh insight channel_snapshot tu data that
- Scheduler: start/stop OK

## API
- GET /os UI
- GET /os/health DB health
- GET /os/api/summary Dashboard
- GET /os/api/cycles POST List/Create cycles
- GET /os/api/videos
- GET /os/api/metrics
- GET /os/api/insights
- GET /os/api/decisions
- GET /os/api/tool_runs
- GET /os/api/tools Proxy 117-tool registry
- GET /os/api/settings
- POST /os/api/run_cycle Chay 1 vong PDCA
- POST /os/api/check/ingest Ingest metrics
- POST /os/api/do/run?tool=X Chay tool
- GET /os/api/scheduler
- POST /os/api/scheduler/start?interval_sec=N
- POST /os/api/scheduler/stop

## Buoc tiep (P5 - Autonomy)
- Bat scheduler tu UI
- Guardrails chat luong truoc khi publish
- Alert khi cycle loi
- A/B experiments tren topic/format

## Ghi chu ky thuat moi truong
- Tool write_file co gioi han ~600 bytes: chia nho file.
- run_python strip leading whitespace: dung chr(32) cho indent.
- run_python strip ki tu * va __: dung + va chr(95).
- ops/control_center.py chi sua 1 cho: include_router sau dong app=FastAPI.


## Scheduler da chay
- API: POST /os/api/scheduler/start?interval_sec=300
- API: POST /os/api/scheduler/stop
- API: GET /os/api/scheduler
