# CODE RULES — DEV

1. Mọi commit phải kèm test (p0_check / selfcheck / ui_accept tùy phạm vi).
2. Không chạm runtime data (state/, output/, logs/, credentials/).
3. Không hard-code đường dẫn máy; dùng ROOT tương đối.
4. Không thêm dependency mới mà không ghi DECISIONS.md.
5. Test phải cô lập: DB tạm, cổng riêng, không bật scheduler production.
6. Không hạ tiêu chuẩn để đạt PASS. Phân biệt PASS/FAIL/SKIP/chưa kiểm chứng.
7. Giữ tương thích ngược entry point cho tới khi PLAN duyệt thay đổi.
