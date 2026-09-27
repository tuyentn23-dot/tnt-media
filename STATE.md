# STATE - TNT MEDIA
Cap nhat: 2026-09-27 (P0 + P1 hardening pass)

KIEN TRUC

pipeline/ (HARD) -> state/pipeline.db
modules/ + ops/ (agent) -> app/ (FastAPI + Web UI + Tray)

TASK STATUS

Task 1 (DONE): Content moi tu RSS (413 items/lan, khong trung)

Task 2 (DONE): Voice da dang + ngat cau tu nhien (6 voices, 4 presets)

Task 3 (DONE): Khong dung dot ngot - fade out 1.8s verified (-52dB)

P0 HARDENING (2026-09-27, commit 9d2cbe1)

Scheduler: interface thong nhat run(interval, stop_event) khop tray.

Scheduler: cron step neo dung mốc (2-10/3 -> [2,5,8]), dau vao loi -> None.

Scheduler: due_now + Asia/Saigon; run_at nhan ca 'YYYY-MM-DD HH:MM' va ISO.

Scheduler: nhan viec nguyen tu _claim_job (2 dispatch -> 1 winner).

Scheduler: pause qua state/paused.flag; MAX_CONCURRENT=2; last_error() surfaced.

Scheduler log: logs/scheduler.log (khop ten UI doc).

Runner: cancelled khong bi ghi de thanh done.

Publish: bo force bypass approval/transition.

Selfcheck: sua file target cho write_api/phase5_api/api_run_schedule/publish_wired.

viral_followup: missing -> 'unknown'; bo forecast views 24h bia dat.

.gitignore: bo ops/*.py, *.txt, index.html, requirements.txt; them WAL/SHM chinh xac.

P1 HARDENING (2026-09-27)

UI 7777: bo CDN, dung /ui/tnt.css va /ui/tnt-alpine.js (offline).

UI 7777: banner mat ket noi + auto retry; health hien thi OFFLINE.

UI 7777: luu publish_mode qua /api/config, doc lai sau restart.

UI 7777: nut Xem + modal video preview tai buoc duyet.

UI 7777: Refresh All khong nhan setInterval (guard this._tick).

Server: /api/health co app/version/scheduler_error.

Server: /api/config GET/POST; /api/media/preview/{pub_id} gioi han output|work.

Selfcheck: them ui_local_assets + api_config_preview (27 PASS).

KIEM THU (evidence)

python tests/p0_check.py -> 22 PASS / 0 FAIL (gom P0 + P1 static + DB copy integrity).

python -m pipeline.selfcheck -> 27 PASS / 0 FAIL.

Live HTTP (test server tam): health 200, /ui/tnt.css 200, /ui/tnt-alpine.js 200, /api/config 200, preview missing 404.

CHUA XAC MINH

Thao tac tray Windows that va trinh duyet that (tab, video, JS errors, offline that).

Publish YouTube that; render FFmpeg that.

RENDER SETTINGS (final)

Resolution: 540x960 (do paging file nho)

Format: vertical short (1080x1920 khi du bo nho)

GHI CHU

8 video da publish public (Mialinhcute + vilevi5676)

KHONG xoa video da publish tru khi co lenh rieng
