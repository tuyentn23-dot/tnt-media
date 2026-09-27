# AGENT EXECUTION RULES

1. Một tool action mỗi message; chờ TOOL_RESULT rồi mới bước tiếp.
2. Đọc STATE.md, BRAIN.md, git status, git rev-parse HEAD trước khi sửa.
3. Không git reset --hard, không xóa WAL/SHM để làm sạch Git.
4. Không đăng/xóa video YouTube, không API upload thật, không sửa DB production.
5. Không ghi đè thay đổi chưa commit của người dùng.
6. Không dừng tiến trình ngoài ứng dụng.
7. Khi bị chặn: nói thẳng, không báo DONE dựa trên HTTP 200 hay file tồn tại.
8. Báo cáo cuối phiên: HEAD trước/sau, lỗi tái hiện + bằng chứng, lệnh test + PASS/FAIL/SKIP, thao tác browser/tray thực hiện, phần chưa xác minh.
9. Cảnh giác harness làm hỏng nội dung file ghi qua tool: dùng base64/chr() khi cần giữ nguyên ký tự đặc biệt; kiểm chứng bằng đọc lại byte.
