# AGENT RULES — Hiến pháp làm việc của TNT Media OS

Áp dụng cho MỌI phiên agent. Đọc trước khi làm bất cứ gì.

## 5 QUY TẮC BẤT DI BẤT DỊCH

### QT1 — Mục tiêu trước, giải pháp sau
Trước khi viết gì, tự hỏi: "User muốn KẾT QUẢ gì?" (không phải CÁCH gì).
Kết quả là cái bất biến. Cách là cái thay được.

### QT2 — Chọn cách đơn giản nhất chạy được
Thứ tự ưu tiên (chọn bậc THẤP NHẤT đủ dùng):
1. File tĩnh (JSON/MD) — đọc được là xong
2. Script 1 lần (python x.py) — cần logic
3. Script chạy nền — chỉ khi bắt buộc
4. Server / daemon — chỉ khi 3 cái trên không đủ
5. Cloud — chỉ khi máy tắt vẫn cần chạy

Không được nhảy bậc. Bậc 2 đủ thì KHÔNG dùng bậc 4.

### QT3 — Fail 2 lần thì ĐỔI CÁCH
Cùng 1 cách fail 2 lần:
- KHÔNG sửa tiếp cách đó
- DỪNG, phân tích vì sao fail
- Chọn cách khác ở bậc thấp hơn (QT2)

### QT4 — Tôn trọng giới hạn kênh
Wrapper này có giới hạn VẬT LÝ (xem WRAPPER_RULES.md).
Khi chọn cách, hỏi: "Cách này có vượt giới hạn không?"
Nếu có → chọn cách khác. KHÔNG cố lách.

### QT5 — Fail 3 lần thì BÁO USER
Sau 3 lần thử fail:
- DỪNG
- Nói thẳng: "Cách X không khả thi. Đề xuất cách Y."
- Để user quyết
Không tự đâm tiếp.

## CHECKLIST TRƯỚC MỌI VIỆC LỚN

1. Kết quả user muốn là gì? (1 câu)
2. Cách đơn giản nhất đạt kết quả đó? (bậc thấp nhất — QT2)
3. Cách đó có vượt giới hạn kênh không? (QT4)
4. Nếu fail 2 lần, tôi đổi sang cách nào? (QT3)
5. Khi nào tôi báo user? (sau 3 lần — QT5)

## NGUYÊN TẮC BỔ SUNG

- Kết quả > Cách. Kết quả > Code đẹp. Kết quả > Sự hoàn hảo.
- Cái gì chạy được và đơn giản > cái gì đẹp và phức tạp.
- Ghi mọi quyết định vào file để phiên sau đọc. Trí nhớ agent KHÔNG tồn tại giữa các phiên.
- Nếu không chắc, chọn cách đơn giản hơn và hỏi user.
- Không bao giờ sửa file ngoài workspace media/ mà không hỏi.
