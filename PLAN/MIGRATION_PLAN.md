# MIGRATION PLAN — Tái cấu trúc PLAN/DEV/RUN

> Trạng thái: CHỜ DUYỆT — chưa di chuyển vật lý để tránh phá hệ thống đang chạy.
> Nguyên nhân trì hoãn: đổi đường dẫn source/runtime phá sys.path và imports; cần app DỪNG + test sau mỗi bước.

## Điều kiện tiên quyết
1. Dừng tray + server + scheduler + mọi python.exe của app.
2. Backup state/pipeline.db + WAL.
3. Commit sạch (git status trống).
4. Có bản backup toàn workspace (zip).

## Giai đoạn 0 — Chuẩn bị hằng số đường dẫn
Tạo paths.py (hoặc dùng env) làm nguồn duy nhất cho:
- ROOT (workspace)
- DEV_ROOT, RUN_ROOT
- DB_PATH = RUN/state/pipeline.db
- CRED_DIR = RUN/credentials
- OUTPUT_DIR = RUN/output, LOG_DIR = RUN/logs
Mọi module import từ đây, KHÔNG hard-code.

## Giai đoạn 1 — Di chuyển RUNTIME (ít rủi ro nhất)

mkdir RUN
move state RUN\state
move output RUN\output
move logs RUN\logs
move backups RUN\backups
move work RUN\work
move cloud_media RUN\cloud_media
move library RUN\library
move music_bank RUN\music_bank
move movies RUN\movies
move memory RUN\memory

Sau đó tạo junction để đường dẫn cũ vẫn trỏ đúng (Windows, cần quyền):

mklink /J state RUN\state
mklink /J output RUN\output
...

→ Code cũ vẫn chạy, không cần sửa ngay. Dần chuyển sang dùng paths.py.

## Giai đoạn 2 — Di chuyển SOURCE vào DEV

mkdir DEV\src
move pipeline DEV\src\pipeline
move modules DEV\src\modules
move app DEV\src\app
move ops DEV\src\ops
move os_app DEV\src\os_app
move analytics DEV\src\analytics
move src DEV\src\core
move tests DEV\tests
move scripts DEV\scripts
move tools DEV\tools

Cập nhật:
- Mọi sys.path.insert(0, ROOT) -> trỏ DEV\src.
- Entry points (tray/server/runner) -> đặt trong RUN/app hoặc gọi qua DEV.

## Giai đoạn 3 — Dọn tài liệu vào PLAN

move *.md PLAN\ (trừ README gốc)
move docs PLAN\docs


## Giai đoạn 4 — Kiểm thử sau mỗi bước
- python DEV/tests/p0_check.py -> 21 PASS
- python -m pipeline.selfcheck -> 27 PASS
- python DEV/tests/ui_accept.py -> TITLE/TABS/JS_ERRORS
- Chạy thử 1 render + 1 publish MOCK.

## Rollback
- Nếu fail: di chuyển ngược theo log; khôi phục junction; restore DB backup.

## Rủi ro & giảm thiểu
| Rủi ro | Giảm thiểu |
|---|---|
| Phá import | Junction + paths.py + test từng bước |
| Mất dữ liệu runtime | Backup trước, không xóa |
| Server đang chạy | Dừng hết trước khi move |
| Publish ngoài ý muốn | Không bật scheduler khi migrate |
