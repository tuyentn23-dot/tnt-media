# HANDOFF - PHIEN P0 HOAN THANH

> Cap nhat: 2026-09-27
> Trang thai: P0 DONE, he thong hoat dong on dinh

## 1. Tom tat

Da hoan thanh P0: backend + tray + render + publish hoat dong end-to-end.
Da render + publish video that (privacy=private).

## 2. Bang chung end-to-end

- Render: output/chMialinhcutelive_gacha_daa30675c720260927_091507.mp4 (1080x1920)
- Publish: youtube_id=yMZMm76WQe4 (private), score=80, DB status=published
- Multi-channel: render OK cho ca Mialinhcute va vilevi5676
- Scheduler: cron chinh xac, dispatch spawn runner
- Recovery: reset job ket running
- Backup: WAL-safe, verify OK

## 3. File da sua (P0)

### Pipeline
- pipeline/job.py - them uuid job_id, transition tables
- pipeline/runner.py - lap du kinds, validate output, khong gan published gia
- pipeline/scheduler.py - dispatch_job spawn runner process
- pipeline/recovery.py - MOI, recover stale jobs

### App
- app/server.py - import publish router
- app/_routes_publish.py - MOI, endpoint publish + kiem tra approved
- app/tray.py - single-instance, health check, log, menu day du

### Ops
- ops/live_content.py - strip HTML, khong doc URL, filter noi dung cam
- ops/channel_loader.py - wire filter_items
- ops/backup_state.py - MOI, backup WAL-safe
- ops/ffmpeg_render.py - KHONG sua, da dung tot (1080x1920)

### Modules
- modules/render/video.py - chuyen sang dung ffmpeg_render (thay channel_style hong)

### Channels
- channels/Mialinhcute/channel.json - voice female_north
- channels/vilevi5676/channel.json - voice female_north

## 4. Quy trinh ghi file QUAN TRONG

CANH BAO: tool write_file STRIP dau gach duoi kep (__) khi ghi file Python.

Quy trinh dung:
1. Viet file voi placeholder FILEMARK cho file, MAINMARK cho main
2. Chay: python ops/_patch.py <path>
3. Verify: python -c "import ast; ast.parse(open('<path>').read())"

Hoac viet lai byte-level: xem ops/fix*.py de vi du.

## 5. Lenh thuong dung

- Mo tray: python app/tray.py
- Dashboard: http://127.0.0.1:7777/ui/index.html
- Render: python -m pipeline.runner --channel <id> --kind <kind>
- Dry-run: them --dry-run
- Backup: python ops/backup_state.py --verify
- Recover: python -c "from pipeline import recovery; recovery.recover_stale_jobs()"

## 6. Con lai (P1/P2)

- Topic mapping RSS qua rong (showbiz -> gacha)
- UI duyet chua co player xem video
- UI 13 tab can to chuc lai
- Caption chua bam timestamp TTS
- Music chua chon theo cam xuc
- Windows Startup chua tich hop
- channel_style.py van hong (da bypass bang ffmpeg_render)

## 7. Video da publish (private)

- youtube_id: yMZMm76WQe4
- privacy: private
- URL: https://youtu.be/yMZMm76WQe4
- KHONG xoa tru khi co lenh rieng
