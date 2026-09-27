# DECISIONS (ADR) — TNT MEDIA OS

## ADR-001: Đưa runtime ra khỏi Git
- Ngày: 2026-09-27
- Bối cảnh: state/pipeline.db, archives, cloud_media bị track.
- Quyết định: git rm --cached (giữ file trên đĩa), thêm vào .gitignore.
- Hệ quả: tracked giảm 1311 -> 1032; DB không còn trong lịch sử commit mới.

## ADR-002: Sửa interface key cho module
- Bối cảnh: content.viral_pack4 và render.viral_story_15s thiếu key 'interface'.
- Quyết định: thêm "interface": "run(ctx) -> dict" vào MODULE dict.
- Hệ quả: selfcheck 27/27.

## ADR-003: Sửa lỗi console UI
- Bối cảnh: 2 lỗi "Unexpected token '}'" từ Alpine.
- Nguyên nhân: backslash-escaped single quotes (\') bên trong attribute double-quoted (dòng 47, 83).
- Quyết định: bỏ backslash, dùng nháy đơn trực tiếp.
- Hệ quả: JS_ERRORS 0 (xác minh qua ui_accept sau khi kill stale server cổng 7787).
- Lưu ý: lỗi cũ tái hiện do server cũ còn giữ cổng; cần kill listener trước khi test.

## ADR-004: Tách PLAN/DEV/RUN
- Quyết định: áp dụng mô hình 3 hệ thống độc lập; chờ người dùng duyệt luật trước khi di chuyển thư mục.
