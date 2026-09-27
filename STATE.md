# STATE - TNT MEDIA
Cap nhat: 2026-09-27 (P0 hardening pass)

## KIEN TRUC
pipeline/ (HARD) -> state/pipeline.db
modules/ + ops/ (agent) -> app/ (FastAPI + Web UI + Tray)

## TASK STATUS
- Task 1 (DONE): Content moi tu RSS (413 items/lan, khong trung)
- Task 2 (DONE): Voice da dang + ngat cau tu nhien (6 voices, 4 presets)
- Task 3 (DONE): Khong dung dot ngot - fade out 1.8s verified (-52dB)

## P0 HARDENING (2026-09-27)
- Publish: bo force=True, chan khi video_health exception (c4e8e5a)
- Chong dang trung: UPDATE atomic WHERE status cu (8c80656)
- Render race: tempfile.mkdtemp rieng moi job (0d41563)
- Route trung: xoa handler publish cu trong server.py (871fa6f)
- Backup: dung SQLite Backup API (3703fe0)
- Pause/Resume: flag state/paused.flag, khong toggle channels.enabled (c4921b6)
- channel_style.py: sua indent, bo fallback chet trong runner (534066e)
- Scheduler: full cron 5 field + */n + run_at one-shot (8e46797)
- Tray: them menu Xem log / Backup ngay (60a247c)
- UI 7777: sua quote bug cot Time va Log (bf22f45)
- Runner: heartbeat cap nhat jobs.updated_at moi 60s (0aaf842)

## RENDER SETTINGS (final)
- Resolution: 540x960 (do paging file nho)
- Format: vertical short (1080x1920 khi du bo nho)

## GHI CHU
- 8 video da publish public (Mialinhcute + vilevi5676)
- KHONG xoa video da publish tru khi co lenh rieng
