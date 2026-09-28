# BACKLOG — TNT MEDIA OS

## P0 — Khẩn (đang chặn vận hành)

### B1. YouTube API quota exceeded (clip đăng failed)
- Triệu chứng: publications status=failed, error=HttpError 403 ... exceeded your quota
- Nguyên nhân gốc: YouTube Data API v3 quota = 10.000 units/ngày, tính theo Google Cloud project (KHÔNG theo kênh). Mỗi videos.insert (upload) tốn ~1600 units → tối đa ~6 upload/ngày cho TẤT CẢ kênh dùng chung client_secrets.json.
- Vì sao "mới đăng mà hết": app đăng nhiều kênh (6 kênh) cùng lúc → vượt ~6 upload/ngày rất nhanh. Các lần thử lại cũng tiêu quota.
- Hướng xử lý:
 1. Giới hạn số upload/ngày trong scheduler (mặc định ≤5) — tránh vượt quota.
 2. Tách mỗi kênh/nhóm kênh sang project Google Cloud riêng (mỗi project 10k units) để tăng hạn mức.
 3. Xin tăng quota (YouTube API audit form).
 4. Hiển thị quota còn lại + số upload hôm nay trên Dashboard.

### B2. Module render.short không tồn tại
- Triệu chứng: job kind=render.short → module_error: render.short: No module named 'render'
- Nguyên nhân: runner tra modules/render/short.py — không có. Chỉ có render.video, render.viral_15s, render.viral_story_15s, render.music.
- Hướng xử lý: tạo modules/render/short.py (alias gọi ops.ffmpeg_render.render) HOẶC đổi job kind sang module hợp lệ.

### B3. Cửa sổ cmd đen chớp khi render/publish
- Nguyên nhân: ops/_no_window.py bị thiếu → import thất bại im lặng → subprocess hiện console.
- Đã fix code: ops/_no_window.py + ops/__init__.py + ops/no_window.py + sitecustomize.py (patch Popen/os.system/os.popen).
- Còn lại: restart tiến trình đang chạy (server 7777 PID 17116 khởi động trước fix).

## P1 — Nên làm
- B4. Chống double-upload (atomic claim đã có, cần test kỹ publish race).
- B5. Dashboard hiển thị quota YouTube còn lại.
- B6. Tắt/dọn 7 scheduled task TNT trùng lặp với scheduler nội bộ.
- B7. Dọn debug files, chuẩn hóa .gitignore.

## P2 — Sau
- B8. Tái cấu trúc vật lý PLAN/DEV/RUN (xem MIGRATION_PLAN.md).
- B9. Nghiệm thu tray.
- B10. Render mẫu cách ly.
