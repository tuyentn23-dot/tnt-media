# CHANGELOG - XEM _archive_CHANGELOG.md cho lich su cu

## 2026-09-22 (phien Noi A->B + YC2/3/4/7 + Fix publish)
- Noi Nhanh A (memory/tnt_media.db) vao Nhanh B (system/state.db): ops/sync_a_to_b.py, tich hop vao state_sync.py
- YC3: viet lai ops/trend_scan.py (Google Suggest free) -> 170 trends
- YC4: viet lai ops/decision_engine.py (trends -> decisions, idempotent)
- YC2: ops/idea_generator.py (Groq openai/gpt-oss-120b) -> 6 y tuong moi
- YC7: them GET /os/api/state doc Nhanh B vao dashboard
- YC1: ops/decision_to_publish.py (dry-run mac dinh)
- FIX BUG moviepy: shim with_* -> set_* trong ops/compat.py (venv la moviepy 1.0.3)
- FIX script MIA: them 5 topic co dau tieng Viet vao config/scripts_vi.json
- FIX nhac: _music_for chon tu music_bank/ (221 bai) thay vi 6 bai library
- PUBLISH TEST: Mialinhcute 4 clip (anime lf5wVD-JXlU, roblox zVLfPtk3E5U, cute_animals o-7fNEJKNFE, meme VJv21IYSqvk)

## 2026-09-21 (phien Kids + ViLe Vi + Anime AI)
- 5 video ViLe Vi facts da dang (octopus/moon/shark/brain/heart)
- 5 video Mia kids da dang (gacha/roblox/anime/cat/pikachu)
- 8 video Mia teen da dang (pikachu/gacha/bully/cold/wheel/meme/drama/cool)
- Tools moi: gacha_anime_render, anime_ai_render, build_mia_kids, build_vile_short
- Content moi: mia_content_kids, vile_content, content_v2, gacha_viral_pack
- QG rieng cho ViLe Vi: quality_gate_vile
- Fix: font Segoe UI (khong Arial Black), caption drawtext dung relative path

Xem SESSION_HANDOFF.md de biet chi tiet day du.

## 2026-09-22 (phien YC1: noi decision B vao autopublish)
- ops/autopublish_runner.py: them _decision_topic() doc decision_to_publish.choose(3), dung footage lam topic build video; fallback topic_picker khi khong co decision
- Da compile OK; _decision_topic tra ve footage hop le

## 2026-09-22 (phien dang 4 clip moi - 2 kenh dung style)
- Mialinhcute: anime_sailormoon https://youtu.be/SS13ejNumtU | roblox_piggy https://youtu.be/0Bvwg9uh8ws (score 80)
- vilevi5676: v_market_morning https://youtu.be/xeieMfkPqFk | v_rain_saigon https://youtu.be/ohv0anIryiw (score 80)
- Dung ops/channel_producer.run_many(cid, limit=2, live=True): content_db.json rieng tung kenh + quality gate + token rieng
- state_sync A->B: videos=255 publishes=235 analytics=26

## 2026-09-22 (phien 4 - hoan tat 7 YC)
- YC1 XONG: ops/scheduler_cc.py (cron 5 truong, doc scheduleCron tung kenh, chay channel_producer.run_many)
- YC4 XONG: ops/weights_tuner.py (hoc tu memory/tnt_media.db metrics) + decision_engine dung weights
- YC5 XONG artifacts: deploy/oracle_setup.sh, tnt-scheduler.service, tnt-dashboard.service, README_ORACLE.md
- YC6 XONG: ops/evolution.py - 3 cap (A/B prompt, weight tuning, tool gen+approve)
- YC7 XONG: ops/os_api.py (quota per channel + /api/quotas + /api/os/state) moc vao control_center
- YC2/YC3 da XONG tu truoc
- Tat ca module compile OK; state_sync A->B: videos=255 publishes=235 tools=385

## 2026-09-23 (phien 5 - test 8 clip moi, 4/kenh dung rule)
- Mialinhcute: roblox_arsenal xiSXKm_KJTg | roblox_jailbreak YboaI7Rmfdc | animal_panda 3U8RdfVjLqM | animal_fennec RogmlM6mTgI (score 80)
- vilevi5676: v_why_dejavu MAzJCIPN5dw | v_why_hair_gray rw5tC9jX5_4 | moon_drift tykeuQ85qk4 | octopus3heart 2wFyx_7XuJM (score 80)
- Tao requirements.txt, deploy/push_to_vm.sh, deploy/CHECKLIST.md cho YC5
- YC5 cho tai khoan Oracle (cho credit card)
- state_sync A->B: videos=263 publishes=243

## 2026-09-23 (phien 6 - chuan bi deploy cloud khong the)
- Tao git repo RIENG trong media/ (tach khoi D:/TNT_AI), commit 1065 files, 0 secrets
- Chan secrets: token.pickle, config/client_secrets.json, .env, *.db
- cloud_media/ 313MB (36 clip + 10 nhac) cho cloud build
- Dockerfile + start.sh + docker-compose + requirements.txt
- deploy/prepare_cloud_media.py, git_push_cloud.sh, README_CLOUD.md
- Huong dan: ClawCloud (~8GB, khong the) / Zeabur / Koyeb(512MB->OOM)
- Buoc tiep: user push len GitHub -> deploy ClawCloud

## 2026-09-23 (phien 6 - chuan bi deploy cloud khong the)
- Tao git repo RIENG trong media/ (tach khoi D:/TNT_AI), commit 1065 files, 0 secrets
- Chan secrets: token.pickle, config/client_secrets.json, .env, *.db
- cloud_media/ 313MB (36 clip + 10 nhac) cho cloud build
- Dockerfile + start.sh + docker-compose + requirements.txt
- deploy/prepare_cloud_media.py, git_push_cloud.sh, README_CLOUD.md
- Huong dan: ClawCloud (~8GB, khong the) / Zeabur / Koyeb(512MB->OOM)
- Buoc tiep: user push len GitHub -> deploy ClawCloud

## 2026-09-23 - Phase 0 + Phase 1 (Pipeline Foundation)

### Them moi
- PIPELINE_SPEC.md (8327 bytes) - Kien truc + DB schema + API + self-evolution
- AGENT_RULES.md + PHAN II-V - Ky luat pipeline cho moi phien
- ops/publish_cleanup.py - Xoa video da dang (Task B)
- pipeline/state.py - SQLite API, 9 bang + 3 index
- pipeline/migrate.py - Import 4 ledger cu -> DB
- pipeline/selfcheck.py - Health check (5 PASS)
- state/pipeline.db - NGUON SU THAT DUY NHAT (72 publications)

### Cau truc moi
- pipeline/ (HARD, cam sua)
- modules/ (agent lam viec o day)
- app/ (mini app - chua lam)
- config/ (schema)
- state/ (DB + backup)

### Migration
- 4 ledger cu -> bang publications trong state/pipeline.db
- 72 ban ghi (Mia 26, ViLe 17, global 12, whatif 1, None 16)

### Xoa
- 38 file video da dang khoi output/ (1068 -> 1030 items)

## 2026-09-23 - Phase 2 (Runner + API)

### Them moi
- pipeline/job.py - Job dataclass (to/from json, validate)
- pipeline/modules_loader.py - Discover + validate MODULE dict
- pipeline/runner.py - Orchestrator chinh (CLI --job-json / --channel / --dry-run)
- app/server.py - FastAPI read-only, port 7777
- app/_test_api.py - Test 6 endpoints (all 200)
- modules/content/loader.py - Module mau (MODULE v1.0.0)

### API endpoints
- GET /api/health - 72 pubs, 3 jobs
- GET /api/channels
- GET /api/publications?limit=N&channel_id=X
- GET /api/jobs?limit=N
- GET /api/quota
- GET /api/modules

### Selfcheck
- Mo rong tu 5 -> 8 checks (them pipeline_phase2, app_server, modules_discoverable)
- Ket qua: 8 PASS / 0 FAIL

### Deps moi
- httpx 0.28.1 (cho TestClient)

## 2026-09-23 - Phase 3 (Web UI)

### Them moi
- app/ui/index.html - SPA (Tailwind + Alpine.js CDN, 4746 bytes)
- pipeline/import_channels.py - Import channels/*.json vao DB
- app/server.py - Mount /ui static, GET / -> redirect /ui/index.html

### UI tabs
- Dashboard: pubs/jobs/channels count + modules table
- Channels: bang 3 kenh
- Publications: 72 ban ghi + link YouTube
- Jobs: 3 job

### Data imported
- 3 channels: Mialinhcute, MinhTriet-AI, vilevi5676

### Selfcheck
- 8 -> 10 checks (them ui_index, channels_imported)
- 10 PASS / 0 FAIL

### Test
- Server that: uvicorn port 7777, /api/health 200, /ui/index.html 200
- TestClient: root 307 redirect, /ui 200

### Bug fix
- glob *.json bi strip * -> fix bang chr(42)
- x-show attribute double-quote long -> fix bang single-quote ngoai

## 2026-09-23 - Phase 4 (Write API + Job Builder)

### Them moi
- POST /api/jobs - tao job (validate + insert DB)
- DELETE /api/jobs/{id} - huy job
- POST /api/cleanup - goi publish_cleanup.py (dry-run/force)
- UI tab Job Builder - form channel/kind/topic/count/approval + nut Create
- UI tab Publications cleanup button

### Test E2E
- Server that port 7777
- POST /api/jobs -> 200 job_id
- GET /api/jobs -> 200 3 jobs
- DELETE /api/jobs/{id} -> 200 deleted=1
- POST /api/cleanup?force=false -> 200 dry-run
- UI: co Create Job + submitJob

### Selfcheck
- 10 -> 12 checks (write_api, ui_job_builder)
- 12 PASS / 0 FAIL

### Bug fix
- JS headers {{...}} -> {...}
- Builder block chen truoc </main>

## 2026-09-23 - Phase 5 (Approval + Analytics + Assets)

### API moi
- GET /api/pending - publications status=rendered
- POST /api/publications/{id}/approve
- POST /api/publications/{id}/reject (ghi audit)
- GET /api/audit?limit=N
- GET /api/assets?kind=X
- GET /api/analytics (total, by channel, by status)

### UI moi
- Tab Approval: bang pending + nut Approve/Reject
- Tab Analytics: total + by channel
- Tab Audit: bang audit log

### Selfcheck
- 12 -> 14 checks (phase5_api, ui_phase5)
- 14 PASS / 0 FAIL

### E2E
- 4 endpoint 200, analytics total=72, UI co 4 tab moi

## 2026-09-23 - Phase 6 (Tray Integration)

### Them moi
- app/tray.py - Tray app moi (pystray)
 Menu: Open Manager, Start Server, Show Status, Quit
- run_tray_new.bat - wrapper Windows

### Chung nang
- Open Manager: mo browser http://127.0.0.1:7777/ui/index.html
- Start Server: spawn app/server.py (DETACHED_PROCESS)
- Show Status: query DB, in pubs/jobs
- Quit: kill server + icon.stop()

### An toan
- Chay SONG SONG voi ops/tray_app.py cu
- Khong dung tray cu -> co the rollback

### Selfcheck
- 14 -> 15 checks (tray_app)
- 15 PASS / 0 FAIL

## 2026-09-23 - Phase 7-10 (Scheduler, Notify, Quota, MVersion)

### Phase 7 - Scheduler
- pipeline/scheduler.py - tick moi 60s, parse cron 5-field
- Tu dong tao job tu channels.schedule.cron

### Phase 8 - Notification
- pipeline/notify.py - log JSON + job_failed/job_done/quota_low
- logs/notify.log

### Phase 9 - Quota
- pipeline/quota.py - 10k units/ngay, UPLOAD_COST=1600
- get/consume/can_upload/reset

### Phase 10 - Module versioning
- pipeline/mversion.py - snapshot/rollback/list_versions
- state/snapshots/*.bak

### Wire
- runner.py: import notify + quota, notify sau run_job

### Selfcheck
- 15 -> 19 checks (them phase7-10)
- 19 PASS / 0 FAIL

### E2E
- 10/10 API endpoints 200
- 8/8 UI tabs

## 2026-09-23 - P1 (Real Modules)

### Them moi
- modules/render/video.py - wrapper channel_style.build_styled
- modules/render/music.py - wrapper music_mixer
- modules/voice/tts.py - wrapper voice_engine
- modules/publish/youtube.py - wrapper os_publish

### Wire
- pipeline/runner.py: dung modules_loader.discover() + _call()
- Fallback ve ops.* neu module fail

### Modules discover
- 5 modules: content.loader, render.video, render.music, voice.tts, publish.youtube
- Tat ca valid=True

### E2E
- 10/10 endpoints 200
- 8/8 UI tabs
- Selfcheck: 19/0 PASS

## 2026-09-24 - Tray Migration

### Done
- Disable tray cu: TNT_Media_OS.vbs -> .disabled
- Tao deploy/run_tray_v2.vbs (tro app/tray.py)
- Cai vao Startup: TNT_Media_OS_v2.vbs

### Verified
- Tray moi chay that: PID pythonw.exe app\tray.py
- Autostart cai dung cho
- Selfcheck 19/0 PASS

### Reboot se tu chay tray moi

## 2026-09-24 - Tray Auto-Spawn Server

### Nang cap app/tray.py
- Them ham port_open() (socket check)
- Them ham spawn_server() (DETACHED_PROCESS + wait port)
- main(): tu dong spawn server khi tray khoi dong
- Open Manager / Start Server deu dam bao server UP

### Verified
- Tray moi chay -> server port 7777 tu dong LISTENING
- /api/health -> 200 {publications:72, jobs:6}
- /ui/index.html -> 200
- Selfcheck 19/0 PASS

### Autostart
- TNT_Media_OS_v2.vbs (Startup) -> app/tray.py -> auto spawn server

## 2026-09-24 - Pipeline E2E Test (Dragonball)

### Flow da test
1. POST /api/jobs -> tao job_20260924_074931 (pending)
2. python -m pipeline.runner --channel Mialinhcute --kind anime (detached)
3. Render video: chMialinhcute_anime_dragonball_20260924_075149.mp4 (3.07 MB)
4. Ghi publication #95 vao DB, status=rendered
5. Job status -> pending_approval
6. POST /api/publications/95/approve -> 200, status=approved

### Ket qua
- Render pipeline hoat dong (channel_style.build_styled qua module render.video)
- Approval workflow hoat dong (rendered -> approved)
- Dedup signature hoat dong (job 075149 cung dragonball -> skip)
- Notify hoat dong (logs/notify.log)

### Luu y
- Render 1 video mat ~2 phut -> tool run_terminal 60s timeout
- Can spawn detached + poll DB (khong cho truc tiep)

## 2026-09-24 - UI Actions + Edge App Window

### Tray (app/tray.py)
- Mo cua so app rieng bang Edge/Chrome --app (khong phai browser tab)
- Window 1000x700, profile rieng tai state/browser_profile
- Menu: Dashboard (default) / Start Server / Show Status / Quit

### API moi (app/server.py)
- POST /api/jobs/{id}/run - chay job ngay (detached)
- POST /api/jobs/{id}/schedule - hen gio (run_at)
- POST /api/publications/{id}/publish - dang len YouTube

### UI moi (app/ui/index.html)
- Job Builder: 2 nut Create / Create + Run ngay
- Jobs table: nut Run / Schedule / Del tung job
- Publications table: nut Publish
- JS: publishPub, runJob, scheduleJob, deleteJob

### Verified
- E2E: create -> run -> schedule -> delete deu 200
- Selfcheck: 21/0 PASS

## 2026-09-24 - Full Features (6/6)

### 1. Publish that (YouTube)
- POST /api/publications/{id}/publish goi ops/os_publish.publish()
- Update status -> published + luu youtube_id

### 2. Scheduler chay nen
- Thread daemon trong app/tray.py, interval 60s
- Tu dong tick + tao job theo cron

### 3. Edge app window
- --app mode, 1000x700, profile rieng
- Title: TNT Media Manager

### 4. Settings tab
- Publish mode (approve/auto)
- API URL readonly
- Refresh All + Cleanup Output buttons

### 5. Auto-refresh
- setInterval 10s -> loadPublications + loadPending

### 6. Toast notification
- x-show toast, 3s tu dong an
- showToast(msg) JS method

### Selfcheck: 23/0 PASS (them ui_settings_tab, publish_wired)

## 2026-09-24 - Full Control Dashboard (12 features)

### UI tabs moi (2)
- Topics: pool + add/del + idea expander
- Diagnostics: selfcheck button + log viewer + backup + KILLSWITCH

### UI dropdown (yeu cau)
- Kind: dropdown tu channel config + option "Khac" + o nhap custom
- Voice: dropdown HoaiMy/NamMinh/HoaiMyNeural/NamMinhNeural
- Topic: input + nut Idea de goi y hook

### API moi (12)
- GET/POST/DELETE /api/topics
- GET /api/trends
- POST /api/idea
- GET /api/config/voices, /api/config/kinds
- GET /api/diagnostics/selfcheck, /api/diagnostics/logs, /api/diagnostics/logs/list
- POST /api/killswitch
- POST /api/backup, GET /api/backup/list
- GET /api/modules/versions, POST /api/modules/snapshot, POST /api/modules/rollback

### JS methods (12)
- loadTopics, addTopic, delTopic, expandIdea
- runSelfcheck, loadLogs, loadLogFiles
- doBackup, doKill, loadKinds, loadVoices

### Verified E2E
- POST /api/topics -> ok
- POST /api/idea -> 4 hooks
- POST /api/backup -> pipeline_*.db
- POST /api/killswitch -> cancelled 10 jobs
- GET /api/config/kinds?vilevi -> 7 kinds

### Selfcheck: 23/0 PASS

## 2026-09-24 - Complete Dashboard (25/25 checks)

### 13 UI tabs
Dashboard, Channels, Publications, Jobs, Job Builder, Approval,
Analytics, Audit, Topics, Diagnostics, Assets, Modules, Settings

### Features da bo sung
- Tab Assets: browse music_bank (221) + assets (51) + library (45)
- Tab Modules: version list + refresh
- Dashboard: Quota con lai (realtime) + Scheduler status
- Topics: pool + add/del + idea expander
- Diagnostics: selfcheck + log viewer + backup + killswitch
- Dropdown Kind (config + Khac + custom)
- Dropdown Voice (4 options)

### API (13/13 verified)
/api/assets/list, /api/analytics/quota, /api/analytics/feedback,
/api/scheduler/status, /api/audit/log, /api/topics, /api/trends,
/api/config/voices, /api/config/kinds, /api/diagnostics/logs/list,
/api/backup/list, /api/modules/versions, /api/health

### Selfcheck: 25/0 PASS
