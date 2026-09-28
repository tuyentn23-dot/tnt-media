# RUN/ — Khu vực vận hành

Vai trò: chạy trực tiếp, quản lý runtime. KHÔNG sửa source.

## Nội dung thuộc RUN (KHÔNG commit)
- state/ — pipeline.db + WAL/SHM, ui_config.json, scheduler_status.json
- output/ — video render
- logs/ — log runner/scheduler/server
- backups/ — backup DB
- work/ — scratch render
- cloud_media/, library/, music_bank/, movies/ — media nặng
- memory/ — footage cache, tray state (không chứa token)
- credentials/ — client_secrets.json, token.pickle, channels/*/token.pickle (gitignore triệt để)
- _trash/, _attic/, _archive*/ — dọn dẹp
- app/ — entry point chạy (tray.py, server.py)

## QUAN TRỌNG — YouTube API quota
- 1 client_secrets.json = 1 Google Cloud project = 1 quota.
- Quota mặc định: 10.000 units/ngày, mỗi upload ~1600 units -> ~6 upload/ngày cho TẤT CẢ kênh.
- 6 kênh dùng chung project -> rất dễ vượt quota.
- Giới hạn upload/ngày <= 5 trong scheduler.
- Muốn nhiều hơn: tách project riêng mỗi kênh, hoặc xin tăng quota.

## Quy tắc
1. RUN không sửa source.
2. Backup DB trước thao tác rủi ro.
3. Không log token.
4. Test dùng cổng riêng, DB cách ly.

## Lệnh chạy

TNT_LAUNCH.bat # tray + server (pythonw)
python -m uvicorn app.server:app --host 127.0.0.1 --port 7777


## Trạng thái di chuyển
Runtime hiện VẪN ở gốc workspace. Kế hoạch: PLAN/MIGRATION_PLAN.md giai đoạn 1.
