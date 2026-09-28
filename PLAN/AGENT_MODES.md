# AGENT_MODES — 3 chế độ vận hành cho AI Agent (TNT Media OS)

Nguyên tắc bất biến: source ≠ data ≠ release.

Mỗi phiên AI agent PHẢI khai báo mình đang ở chế độ nào trước khi làm bất cứ việc gì.

---

## Tổng quan 3 chế độ

| Chế độ | Vai trò | Được làm | KHÔNG được |
|---|---|---|---|
| PLAN | Lập kế hoạch | Ghi trong PLAN/, phân tích, ra task, viết tài liệu | Chạy code, sửa source, publish, chạm data |
| DEV | Phát triển | Sửa source, viết test cô lập, commit | Chạm runtime data, publish, sửa DB prod |
| RUN | Vận hành | Chạy app, backup, xử lý sự cố, publish theo quy trình | Sửa source |

---

## 1. PLAN mode

Mục tiêu: biến vấn đề/nhu cầu thành task rõ ràng, có thể giao cho DEV.

Được phép:
- Đọc mọi thứ (source, data read-only, logs).
- Ghi/sửa file trong PLAN/.
- Phân tích, thiết kế, chia task.
- Đề xuất phương án, trade-off.

KHÔNG được:
- Chạy code, run_terminal gây thay đổi hệ thống.
- Sửa bất kỳ file source ngoài PLAN/.
- Publish, chạm runtime data.

Đầu ra:
- Tài liệu/task trong PLAN/ (vd PLAN/BACKLOG.md, PLAN/ARCHITECTURE.md).
- Mỗi task ghi rõ: mục tiêu, phạm vi file, tiêu chí nghiệm thu.

---

## 2. DEV mode

Mục tiêu: sửa lỗi, nâng cấp source; mọi thay đổi phải test được và commit rõ ràng.

Được phép:
- Sửa source trong DEV/ (tương ứng pipeline/, modules/, app/, ops/, ...).
- Viết/Chạy test cô lập (DB tạm, cổng riêng).
- Commit với message theo chuẩn type(scope): mô tả.

KHÔNG được:
- Chạm runtime data (state/, memory/, output/, DB prod).
- Publish lên kênh thật.
- Sửa DB production.

Đầu ra:
- Thay đổi source + test đi kèm.
- Commit sạch, có thể revert.

---

## 3. RUN mode

Mục tiêu: vận hành hệ thống thật — chạy app, backup, xử lý sự cố, publish theo quy trình đã duyệt.

Được phép:
- Khởi động/dừng app, tray.
- Backup, khôi phục theo quy trình.
- Xử lý sự cố vận hành.
- Publish theo đúng quy trình đã được duyệt (không tự ý đổi logic).

KHÔNG được:
- Sửa source (kể cả sửa nhanh). Nếu phát hiện lỗi source → báo PLAN, để DEV sửa.

Đầu ra:
- Hệ thống chạy ổn định.
- Báo cáo sự cố → chuyển PLAN/DEV.

---

## Luồng phối hợp


RUN phát hiện vấn đề
 -> PLAN lập task (phân tích, tiêu chí nghiệm thu)
 -> DEV sửa source + test + commit
 -> RUN vận hành / nghiệm thu


Quy tắc chuyển mode:
- Muốn chuyển từ PLAN → DEV/RUN: phải có task rõ ràng trong PLAN/.
- Muốn chuyển từ DEV → RUN: phải commit + test pass.
- RUN phát hiện lỗi source: KHÔNG tự sửa, quay lại PLAN.

---

## API & công cụ hỗ trợ

- GET /api/agent-prompts — trả nội dung prompt copy cho từng mode (plan/dev/run).
- GET /api/agent-modes — trả metadata 3 chế độ.
- Trang copy: /ui/agent_modes.html.
