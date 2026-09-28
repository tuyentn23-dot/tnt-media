# Kênh Mia Linh Cute — Ghi chú vận hành

channelId (YouTube): UCi6CpPa0lExuiMREpEwhY-A

Tên hiển thị: Mia Linh Cute (~2480 subs, cập nhật 2026-09-28)

Token: memory/token_new_channel.json (OAuth, có refresh_token)

Aspect: 9:16, maxSeconds 20, voice HoaiMy (female_cute)

Topics: anime, roblox, cute_animals, meme, gacha

Audience: kids, romance forbidden

Lịch sử publish thật (2026-09-28)
Clip	Topic	YouTube ID	Ghi chú
1	cute_animals	DPbWeG7VOTE	OK
2	anime	5F9ejkOTZII	OK
3	gacha	FQqSnQG59jo	OK
4	roblox	lZ94wMn2DBk	OK sau khi fix resize
VẤN ĐỀ CẦN GIẢI QUYẾT (phiên sau)

Hình ảnh không liên quan nội dung: video anime/roblox dùng footage có sẵn trong library, không phải hình động tự tạo → nhìn chung chung, khó viral.

Cần công cụ tạo hình/video động AI cho các topic không có footage phù hợp (anime, roblox, gacha).

Hiện có: providers/gemini_image_adapter.py (cần GEMINI/GOOGLE key — chưa cấu hình).

ai_composer chỉ là music composer, KHÔNG tạo video.

Chưa có text-to-video adapter.

Title bị mất dấu tiếng Việt khi qua pipeline (vd "The gioi anime" thay vì "Thế giới anime") — do title truyền ASCII. Cần giữ Unicode.

Render rất chậm (~8-15 phút/clip) — xem ops/MODULES.md.
