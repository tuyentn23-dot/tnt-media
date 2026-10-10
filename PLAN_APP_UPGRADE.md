# PLAN NÂNG CẤP TNT MEDIA STUDIO

Đây là kế hoạch nâng cấp app desktop (TNT Media Studio).
Đọc file này khi bắt đầu phiên mới.
Cập nhật: 2026-10-10

ĐÁNH GIÁ HIỆN TRẠNG (5/10)
Tab	Điểm	Vấn đề chính
Dashboard	4/10	Sơ sài, thiếu chart, refresh 5s tốn CPU
Channels	5/10	Không edit, xóa nguy hiểm, không validate
Pipeline	6/10	Style/Length/Schedule không tới backend
Queue	7/10	Thiếu thumbnail, không sort
Jobs	4/10	Thiếu progress, filter
Pubs	5/10	Thiếu Title/Views/Likes
Modules	3/10	Quá sơ sài
Settings	4/10	Thiếu settings thực sự

Cross-cutting: không loading state, không empty state, không shortcut, không background worker.

SPRINT 1 - P0 (Fix bug + UX co ban)
1. Fix Pipeline params
□ 

Style dropdown: lay tu channel config (khong hardcode)

□ 

Gui body['style'] nhu string (khong phai index)

□ 

Gui body['length'] (map index -> 'short'/'long')

□ 

Schedule: luu jobs.run_at that su (khong chi display)

File: desktop_app/views/pipeline.py

2. Bulk confirm dialog
□ 

Xac nhan truoc khi publish N video

□ 

Xac nhan truoc khi schedule N video

□ 

Xac nhan truoc khi reject N video

File: desktop_app/views/queue.py

3. Thumbnail trong Video Queue
□ 

Capture frame dau video bang ffmpeg -> cache

□ 

Hien thi thumbnail trong card

□ 

Placeholder neu chua co

File: desktop_app/views/queue.py + pipeline/thumb_cache.py (moi)

4. Filter + Search
□ 

Jobs: filter status + channel + search id

□ 

Pubs: filter channel + search title

□ 

Queue: search topic

File: desktop_app/views/tables.py + queue.py

5. Progress bar trong Jobs
□ 

Them cot Progress (%) dua vao log_tail

□ 

Highlight job running

File: desktop_app/views/tables.py

SPRINT 2 - P1 (UX nang cao)
6. Background worker
□ 

QThread cho publish/schedule (khong block UI)

□ 

Progress dialog cho bulk action

File: desktop_app/workers.py (moi)

7. Keyboard shortcuts
□ 

Ctrl+R: refresh tab hien tai

□ 

Ctrl+1..8: jump tab

□ 

F5: reload all

□ 

Ctrl+F: focus search

File: desktop_app/app.py

8. Loading spinner
□ 

Spinner khi fetch API

□ 

Disable button khi dang chay

File: desktop_app/widgets.py

9. Pubs table nang cap
□ 

Them cot: Title, Views, Likes, Duration

□ 

Nut Copy link YouTube

File: desktop_app/views/tables.py

10. Dashboard chart
□ 

Bieu do 7 ngay views/ngay (QtCharts)

□ 

Cache selfcheck 60s (khong 5s)

□ 

Card co icon + mau + trend

File: desktop_app/views/dashboard.py

11. Channels edit dialog
□ 

Double-click -> edit dialog

□ 

Validate id, voice format

□ 

Xoa: confirm + type ten kenh

File: desktop_app/views/channels.py

12. Copy YouTube link
□ 

Nut copy clipboard

File: desktop_app/views/tables.py

SPRINT 3 - P2 (Hoan thien chuyen nghiep)
13. State management
□ 

Signal/slot giua views (thay doi o Queue -> Dashboard update)

File: desktop_app/state.py (moi)

14. Repository pattern
□ 

Tach UI khoi API

File: desktop_app/repo.py (moi)

15. Module health + rollback UI
□ 

Hien status OK/FAIL

□ 

Nut rollback version cu

File: desktop_app/views/tables.py

16. Settings day du
□ 

Section API URL, credentials (masked), backup history

□ 

System theme (auto)

File: desktop_app/views/settings.py

17. System tray menu day du
□ 

Them: Run pipeline, View queue, Show stats

File: desktop_app/tray.py

18. Tooltips + accessibility
□ 

Tooltip cho moi button

□ 

Tab order hop ly

File: all views

19. Log viewer voi level filter
□ 

Filter INFO/WARN/ERROR

File: desktop_app/views/settings.py

20. Preferences persistence
□ 

Luu tab cuoi, filter cuoi

File: desktop_app/prefs.py (moi)

QUY TAC

Moi buoc xong phai test app load OK (offscreen)

Commit sau moi Sprint

Cap nhat file nay khi xong tung muc

Uu tien khong pha vo chuc nang hien co
