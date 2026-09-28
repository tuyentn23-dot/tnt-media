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

##-- vids_agent.py -- Google Vids AI video generator (mien phi, KHONG API key)

MUC DICH: tao video AI DONG tu text prompt, mien phi, khong can API key.
Ket noi Chrome that qua CDP (port 9222) da dang nhap Google.

CACH DUNG (3 buoc):
1. Chay launch_chrome.py -> cua so Chrome mo ra.
2. Dang nhap Google (1 lan) trong cua so do.
3. Python: from ops import vids_agent; r = vids_agent.generate(prompt, out_path)

API chinh:
 vids_agent.generate(prompt, out_path, cdp_url=None, reuse_page=False, keep_page=False) -> dict
 - prompt: mo ta video (tieng Anh tot nhat)
 - out_path: duong dan luu MP4 (vd library/vids/clip1.mp4)
 - reuse_page: dung tab Vids dang mo thay vi tao project moi
 - keep_page: giu tab sau khi xong (mac dinh dong)
 - tra ve: {ok, error, path, url}

FLOW TU DONG:
 Mo /videos/create (project moi) -> Create AI videos -> Create from scratch
 -> fill prompt -> chon Portrait 9:16 -> Generate -> doi Insert
 -> File > Download (hover) > MP4 video (mouse click) -> luu ve out_path.

LƯU Ý QUAN TRONG (bai hoc xuong mau):
- LUON tao project MOI (/videos/create) de tranh trang thai cu. reuse_page=True chi khi tab sach.
- Chrome PHAI co --remote-debugging-port=9222 (launch_chrome.py). KHONG headless (Google chan).
- Download MP4: dung Browser.setDownloadBehavior (browser-level CDP) + hover Download + pg.mouse.click().
 JS .click() KHONG trigger download (khong phai trusted gesture).
 Playwright expect_download() KHONG bat duoc download POST qua CDP.
 Page.setDownloadBehavior da deprecated -> phai dung Browser.setDownloadBehavior (browser-level).
- Menu File > Download la SUBMENU: phai hover() roi moi click MP4 (bounding_box roi mouse.click).
- Generate mat ~2-3 phut/video (720p, 10s). Timeout wait_video=300s.
- Gioi han free tier chua ro, theo doi quota.

