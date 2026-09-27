# PHIEN HANDOFF - P0 HARDENING DONE

> Cap nhat: 2026-09-27
> Trang thai: 8/8 loi P0 da fix + commit. Task 1+2+3 van DONE.

---

## PHIEN NAY DA XONG (P0 HARDENING)

### 1. Publish bypass quality gate (CRITICAL)
- Commit c4e8e5a
- app/_routes_publish.py: bo force=True khi goi os_publish.publish
- ops/os_publish.py: video_health exception -> block thay vi pass

### 2. Chong dang trung (CRITICAL)
- Commit 8c80656
- UPDATE atomic: UPDATE ... WHERE id=? AND status=? (cur)
- Neu rowcount != 1 -> 409 conflict

### 3. Temp dir rieng (HIGH)
- Commit 0d41563
- ops/ffmpeg_render.py dong 146 va 173: tempfile.mkdtemp(prefix='render_')
- Het race caption khi 2 job song song

### 4. Route trung (CRITICAL)
- Commit 871fa6f
- Xoa handler /api/publications/{pub_id}/publish cu trong app/server.py
- Chi con route trong app/_routes_publish.py

### 5. Backup API (HIGH)
- Commit 3703fe0
- app/server.py: goi ops/backup_state.backup_sqlite() (SQLite Backup API)
- Khong con shutil.copy2 tren file DB dang WAL

### 6. Pause/Resume (HIGH)
- Commit c4921b6
- app/tray.py: ghi/xoa state/paused.flag
- pipeline/scheduler.py: tick() skip khi flag ton tai
- Khong con UPDATE channels SET enabled=0/1 (anh huong ca kenh)

### 7. File hong (HIGH)
- Commit 534066e
- ops/channel_style.py: sua indent try/except + for body
- pipeline/runner.py: bo fallback chet from ops import channel_style as cs
- Xoa ops/safe_io.py (khong dung, indent loi)

### 8. Scheduler cron day du (MEDIUM)
- Commit 8e46797
- pipeline/scheduler.py: parse_cron 5 field day/month/weekday
- Ho tro */n, danh sach, khoang
- tick() xu ly run_at one-shot job (status='scheduled')

---

## COMMIT LOG PHIEN NAY


bf22f45 fix(P0): UI 7777 quote bug in Time and Log columns
60a247c feat(P0): tray menu adds 'Xem log' and 'Backup ngay' handlers
0aaf842 fix(P0): runner heartbeat updates jobs.updated_at every 60s
8e46797 fix(P0): full cron support (day/month/weekday, */n, run_at)
534066e fix(P0): repair channel_style indent, drop fallback in runner
c4921b6 fix(P0): pause/resume via state/paused.flag
3703fe0 fix(P0): backup API now uses SQLite Backup API
871fa6f fix(P0): remove duplicate publish handler from server.py
0d41563 fix(P0): use tempfile.mkdtemp per render job
8c80656 fix(P0): atomic UPDATE to prevent duplicate publish race
c4e8e5a fix(P0): remove force=True in publish route


---

## CANH BAO KY THUAT (van con hieu luc)

- write_file strip __ (dunder) -> dung placeholder FILEMARK/MAINMARK + patch
- write_file strip * trong string -> dung chr(42) hoac bien STARMARK
- write_file strip leading indent -> dung chr(9)/chr(32) + cong chuoi
- write_file CRLF khac LF -> kiem tra bang src.count(bytes([13])) truoc khi patch
- Patch theo byte index khi grep string khong khop

---

## PHIEN SAU - UU TIEN

1. Dong bo 71 pending_approval -> approved hoac reject
2. Don 534 file tam ops/_*.py (giu lai cac file co ich: _tmp_dump.py)
3. Test full pipeline 1 video end-to-end (render -> quality_gate -> publish dry-run)
4. Kiem tra UI 7777 tren browser that (khong chi curl)
5. Chay pipeline.selfcheck dinh ky
6. Them unit test cho parse_cron, atomic publish, backup
