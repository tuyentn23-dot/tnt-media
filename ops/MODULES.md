# OPS MODULES — Ghi chú kỹ thuật

Mục đích: mỗi lần sửa module, ghi lại vấn đề / nguyên nhân / cách fix / lưu ý cho phiên sau.
Nguyên tắc bất biến: source != data != release.

## compat.py — MoviePy 2.x compatibility shim

Vấn đề: Hệ thống dùng moviepy 2.2.1, nhưng code viết theo API 1.x.
Đã gặp 3 lỗi chặn publish:

| Lỗi | Nguyên nhân | Fix |
|---|---|---|
| set_duration not found | 2.x dùng with_duration | shim set_X = with_X |
| resize not found | 2.x dùng resized | shim resize = resized |
| crop not found | 2.x dùng cropped | shim crop = cropped |

Cơ chế: ops/compat.py monkeypatch alias lên mọi clip class, tự chạy khi import.
Hai shim: installlegacysetters() và installmethodaliases().

LƯU Ý PHIÊN SAU:
- Import ops.compat TRƯỚC khi dùng moviepy.
- Gặp "object has no attribute" với moviepy -> thêm cặp (1x, 2x) vào installmethodaliases.
- KHÔNG dùng moviepy.editor (không tồn tại ở 2.x).

## autopublish_runner.py + auto_publish.py — Publish pipeline

Vấn đề: Publish kênh mia fail 100% với lỗi "already published: animal".

Nguyên nhân gốc: _decision_topic() lấy p[footage] (tên folder) làm topic truyền cho run().
-> Guard _already_published(animal)=True -> chặn mọi lần.

Fix:
- _decision_topic() trả (topic_thật, footage, decision).
- run(topic, footage): topic cho title/guard/DB; footage cho lấy clip + script.
- content_planner.for_topic(footage) vì scripts_vi.json key tiếng Anh.
- Title ưu tiên topic thật nếu có space và dài >15.

LƯU Ý PHIÊN SAU: Phân biệt rõ topic (chủ đề) vs footage (folder clip).

## video_build2.py — Render video

Hiệu năng: ~8-15 phút/clip (14s, 1080x1920, 30fps).
Đã thử tối ưu (numpy blit thay PIL per-frame) -> KHÔNG cải thiện (826s vs 727s).
Kết luận: bottleneck là decode + concat video, không phải overlay.

LƯU Ý PHIÊN SAU: Muốn nhanh -> thay ffmpeg trực tiếp (concat demuxer + overlay filter), bỏ moviepy.

## quality_gate / video_quality

Ngưỡng: duration <= 120s, hook_motion >= 0.5, viral_score >= 0. Gate pass với 14s clip.

## LƯU Ý CHUNG VỀ TOOL AGENT

Bug tool phiên này (đã workaround):
- write_file/run_python gộp nhiều space thành 1 -> build indentation bằng chr(32)*N.
- Nuốt ký tự đặc biệt -> dùng chr() thay vì gõ trực tiếp.
- Nên viết generator script (Python ghi file) cho code phức tạp.
