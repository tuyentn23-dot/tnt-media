# 🚀 BOOTSTRAP — ĐỌC FILE NÀY ĐẦU TIÊN MỖI PHIÊN

⚠️ DỪNG LẠI — Không làm gì trước khi đọc hết file này.
File này đảm bảo AI nhớ lịch sử, không phá hệ thống, không làm lại từ đầu.

1. BẮT BUỘC — Chạy lệnh này đầu tiên
bash
Copy
Download
python -m guardian.agent_boot

Lệnh này in ra:

Trạng thái hệ thống (pipeline, DB, scheduler)

Checklist phiên hiện tại

Cảnh báo file nào cấm sửa

Lịch sử làm việc gần nhất

2. KIẾN TRÚC — Hiểu trước khi làm

Hệ thống có 3 tầng cố định (KHÔNG thay đổi):

Tầng	Thư mục	Ai sửa	Cấm
CONTROL	app/ (FastAPI + UI)	Người	Đừng gọi module trực tiếp
DATA	pipeline/	KHÔNG AI SỬA	Không tự quyết định
DEV	modules/, ops/	Agent	Không tự đăng video

Nguyên tắc vàng:

Control plane KHÔNG BAO GIỜ gọi trực tiếp module

Data plane KHÔNG BAO GIỜ tự quyết định

Dev plane KHÔNG BAO GIỜ tự đăng

3. CẤM SỬA — File/dir không được đụng

Đọc guardian/critical.json để biết danh sách đầy đủ.

Tuyệt đối cấm:

pipeline/* — runner, job, scheduler, state, selfcheck

state/pipeline.db — NGUỒN SỰ THẬT DUY NHẤT

guardian/* — hệ thống bảo vệ

app/server.py, app/tray.py

Chỉ sửa:

modules/content/* — nội dung

modules/render/* — video

modules/voice/* — TTS

modules/publish/* — đăng YouTube

4. QUY TRÌNH BẮT BUỘC — Mỗi phiên
Bước 1: Trước khi làm
bash
Copy
Download
python guardian/guard.py before

→ Snapshot 21 file quan trọng.

Bước 2: Trong khi làm

Xoá file: python guardian/safe_fs.py remove <file> (KHÔNG dùng os.remove)

Sửa file: chỉ trong modules/ và ops/

Commit nhỏ, nhiều lần

Bước 3: Sau khi làm
bash
Copy
Download
python guardian/guard.py verify
python -m pipeline.selfcheck
python -m pytest tests/ -q

→ Cả 3 phải PASS. Nếu không → rollback.

5. LỊCH SỬ — Nhớ đã làm gì

Đọc theo thứ tự:

STATE.md — trạng thái hiện tại

CHANGELOG.md — lịch sử thay đổi

PHIEN_HANDOFF.md — handoff phiên trước

PIPELINE_SPEC.md — spec kiến trúc

KHÔNG ĐƯỢC tạo module mới nếu chưa kiểm tra:

bash
Copy
Download
ls modules/*/  # xem đã có gì
6. CƠ CHẾ BẢO VỆ TỰ ĐỘNG
Cơ chế	File	Khi nào
Pre-commit hook	.git/hooks/pre-commit	Trước mỗi commit
Snapshot	guardian/snapshot.py	Trước khi sửa file quan trọng
Safe remove	guardian/safe_fs.py	Khi xoá file
Selfcheck	pipeline/selfcheck.py	Sau khi sửa code
Test suite	tests/	Trước commit
7. NẾU PHÁT HIỆN LỖI

Ngay lập tức:

bash
Copy
Download
python guardian/snapshot.py restore  # Khôi phục file từ snapshot
git checkout -- <file>               # Hoặc restore từ git

Sau đó:

Ghi vào CHANGELOG.md — mô tả lỗi

Thêm test case vào tests/ để tránh tái diễn

Cập nhật guardian/critical.json nếu cần

8. CHECKLIST 100% — Trước khi tuyên bố hoàn thành
□ 

Đã chạy python -m guardian.agent_boot

□ 

Đã đọc STATE.md, CHANGELOG.md, PIPELINE_SPEC.md

□ 

Không sửa file nào trong pipeline/

□ 

Không xoá file bằng os.remove

□ 

python -m pipeline.selfcheck → PASS

□ 

python -m pytest tests/ -q → PASS

□ 

python guardian/guard.py verify → MISSING: none

□ 

Commit message có prefix đúng (feat:, fix:, chore:)

□ 

Đã cập nhật CHANGELOG.md

□ 

Đã cập nhật STATE.md nếu thay đổi kiến trúc

Nếu bất kỳ mục nào KHÔNG đạt → KHÔNG kết thúc phiên.

9. KHẨN CẤP — Khi hệ thống hỏng
bash
Copy
Download
# 1. Xem snapshot nào có
ls guardian/snapshots/

# 2. Khôi phục
python guardian/snapshot.py restore <snapshot-id>

# 3. Rollback git
git reflog
git reset --hard <commit-tốt>

Cập nhật cuối: 2026-10-04
Phiên bản: 1.0
Bắt buộc tuân thủ: 100%


---

## 10. KẾT THÚC PHIÊN — BẮT BUỘC

bash
python -m guardian.session_end


Lệnh này tự động kiểm tra 3 lớp:
1. guardian verify — critical files còn đủ
2. selfcheck — pipeline hoạt động
3. tests — 17 test PASS

Nếu bất kỳ check nào FAIL → KHÔNG KẾT THÚC PHIÊN.

---

## 11. TÓM TẮT CƠ CHẾ BẢO VỆ

| Cơ chế | File | Khi nào |
|---|---|---|
| Bootstrap | guardian/agent_boot.py | Đầu phiên |
| Snapshot | guardian/guard.py before | Trước khi sửa |
| Safe remove | guardian/safe_fs.py | Khi xoá file |
| Critical files | guardian/critical.json | Mọi lúc |
| Pre-commit hook | .git/hooks/pre-commit | Trước commit |
| Test suite | tests/test_bootstrap.py | Trước commit |
| Session end | guardian/session_end.py | Cuối phiên |


---

## 12. PYTHON VENV — Quan trọng

Hệ thống media/ dùng venv riêng: .venv/ (không dùng venv chung D:/TNT_AI/venv)

### Chạy Python trong media/

bash
# Cách 1: Dùng media.bat
media.bat script.py

# Cách 2: Dùng trực tiếp
.venv\Scripts\python.exe script.py


### Cài package mới

bash
.venv\Scripts\python.exe -m pip install <package>
# Sau đó cập nhật requirements.txt
.venv\Scripts\python.exe -m pip freeze > requirements-lock.txt


### LƯU Ý

- KHÔNG dùng venv chung D:/TNT_AI/venv (sẽ ảnh hưởng dự án RapidAPI, FIVERR, MONOLUX)
- KHÔNG chạy taskkill /IM python.exe (giết tất cả process của mọi dự án)
- Khi cần kill: dùng taskkill /PID <specific_pid>
