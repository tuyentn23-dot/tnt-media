# HANDOFF 2026-10-15 — TNT MEDIA (tổng hợp phiên)

> Phiên này: 2026-10-15. Workspace: D:\TNT_AI\venture_foundry\media

## 1. TRẠNG THÁI HỆ THỐNG

- Server 7777: chạy (PID 8916 — đã restart sau fix caption)
- Chrome CDP 9222: OK
- Desktop app: PID gần nhất 33180 (đã restart với UI compact v3)
- Scheduler: đang chạy
- Ollama 11434: OK (qwen2.5:7b + moondream)

## 2. ĐÃ HOÀN THÀNH PHIÊN NÀY (commits)

| Commit | Nội dung |
|---|---|
| `484b941` | Router analyze + registry visible filter |
| `07e29f1` | force add `_routes_analyze.py` (gitignore chan _ prefix) |
| `c0acd7a` | booster freeze-frame + video_reader + compose voice_express |
| `3bf1e3d` | UI step Phân tích + Advisor panel + i18n |
| `30b1532` | booster freeze-frame (fix đen cuối) |
| `9224b1d` | edge-tts endpoint mới + 6 giọng chuẩn |
| `24a29e2` | auto-boost score 100 |
| `fe6365d` | voice_express + voice_script |
| `717c792` | tích hợp 10 module theo 5 nhóm |
| `004da33` | compact UI grid 3 cột |
| `2dd6bd5` | pipeline compact 1 trang |
| `9eadc52` | compact v3 (bỏ label Mô-đun, hint 1 dòng) |
| `8bacf74` | **fix caption nối câu** (mới nhất) |

### A. Analytics + Advisor
- `ops/studio_analytics.py` (MỚI): fetch_analytics + fetch_comments
- `ops/studio_advisor.py`: analytics_block v2, comments_block v2, ingest_advisor
- `ops/topic_pool.py`: custom pool + ingest_advisor

### B. Flow pipeline
- `modules/render/flow_video.py`: fix approve locator, dismiss_promo, force=True
- `ops/flow_worker.py`: gọi `fv.inner()` thay `create()` (fix recursion vô hạn)
- Download poll size ổn định (fix race 0 bytes)
- **Verify:** video 7.6MB thật, end-to-end OK

### C. Voice
- `modules/voice/edge_tts.py`: patch endpoint mới `api.msedgeservices.com` + 6 giọng (nu_cham/nu_nhanh/nam_cham/nam_nhanh/tu_nhien/em_be)
- `ops/voice_express.py` (MỚI): chia câu + pause + rate/pitch theo loại câu
- `ops/voice_script.py` (MỚI): chuẩn hóa có dấu + tách CTA

### D. Video analysis
- `ops/video_reader.py` (MỚI): trích frames + đo brightness + vision (moondream)
- `ops/scene_reader.py` (đã có sẵn): scene detection + HTML report
- `ops/video_analyzer.py` (MỚI): wrapper gọi scene_reader
- `app/_routes_analyze.py` (MỚI): 3 endpoint /api/analyze/quick, /video, /report
- **Verify:** quick check OK với video test 5s

### E. Booster
- `modules/render/booster.py`: `stop_mode=clone` (freeze frame cuối, hết đen)
- `modules/render/video.py`: wrapper auto-boost score 100
- **Verify:** FINAL_v2.mp4, score 100

### F. Caption (MỚI nhất)
- `modules/render/voice_synth.py`: thêm `proportional_words_by_sentence(sentences, dur, gap=0.15)`
- `modules/render/caption_engine.py`: build_karaoke_ass cắt phrase tại dấu câu (. ! ? …), WrapStyle 0, max_chars 50
- `modules/render/compose.py`: gọi proportional_words_by_sentence
- **Verify đơn vị:** 3 câu → 3 dialogue lines, không nối câu
- **CHƯA VERIFY END-TO-END** (cần chạy compose thật — phiên sau làm)

### G. UI Desktop App
- `desktop_app/views/pipeline.py`: layout compact 1 trang (minH 1674 → 302)
  - Bỏ tab Advisor khỏi sidebar
  - Grid step card 5 cột 1 hàng
  - Bỏ label Mô-đun + msg trong card
  - Hint 1 dòng cắt 70 ký tự
  - Form gom 2 hàng
- `desktop_app/views/advisor.py`: i18n VI/EN đầy đủ
- `desktop_app/app.py`: bỏ add advisor tab
- `desktop_app/strings_vi.json` / `strings_en.json`: +30 key mới

### H. Module system (10 module visible)
- `module_registry.json`: field `visible` + `group`
- `pipeline/job.py`: thêm field `modules`
- `app/server.py`: create_job lưu modules, run_job đọc modules
- `pipeline/runner.py`: đọc job.modules → override style['engine']
- DB migration: thêm cột `modules` (đã backup)

**10 module visible hiện tại:**
- analyze: `analyze.video_analyzer`
- content: `content.ollama`, `content.trend`, `content.manual`
- render: `render.flow_video`, `render.pexels_engine`, `render.mix_core`, `render.gacha`
- voice: `voice.tts`
- publish: `publish.youtube`

## 3. TỒN ĐỌNG PHIÊN SAU

### ƯU TIÊN CAO
1. **Verify caption end-to-end** — chạy compose thật với clip ngắn 10s (`output/_cap_base.mp4` đã tạo sẵn), xem ASS file / output video có mỗi câu 1 khung không
2. **Verify pipeline run thật** — chạy 1 job qua UI, xem modules dict có gửi đúng không (server đã patch, cần test)
3. **Xóa 27 module rác** — đã ẩn khỏi UI nhưng file vẫn còn; cần duyệt danh sách trước khi xóa
4. **Auto-delete video sau đăng** — chưa có tiêu chí (sau N ngày? sau publish OK? giữ bản gốc?)

### ƯU TIÊN TRUNG BÌNH
5. Flow CDP timeout — có lúc Flow fail với timeout 180s, cần kill Chrome + mở lại profile sạch
6. Vision moondream timeout — máy chậm, cần model nhẹ hơn hoặc tăng timeout

### ƯU TIÊN THẤP
7. Fix SyntaxWarning `\\d` trong regex
8. Xem video gacha thực
9. A/B testing hook styles

## 4. TEMP FILES CÒN LẠI

Đã dọn hết `_*.py` ở root. Còn lại:
- `output/_cap_base.mp4` (clip test 10s)
- `_test_cap_e2e.py` (test script caption — cần chạy tiếp)
- `_cap_e2e.log`, `_cap_e2e_stdout.txt` (log test)
- `_cap_e2e.mp4` (output test — có thể chưa tạo)

## 5. FILE QUAN TRỌNG CẦN CHÚ Ý

| File | Chú thích |
|---|---|
| `ops/voice_express.py` | Chia câu + pause + cảm xúc |
| `ops/voice_script.py` | Chuẩn hóa tiếng Việt có dấu |
| `ops/video_reader.py` | Đọc video + phát hiện lỗi |
| `ops/video_analyzer.py` | Wrapper scene_reader |
| `modules/render/caption_engine.py` | Karaoke ASS — **vừa patch cắt câu** |
| `modules/render/voice_synth.py` | Có `proportional_words_by_sentence` |
| `modules/render/booster.py` | Freeze frame cuối |
| `modules/render/video.py` | Auto-boost wrapper |
| `modules/voice/edge_tts.py` | Patch endpoint + 6 giọng |
| `desktop_app/views/pipeline.py` | UI compact 1 trang |

## 6. CÁCH KHỞI ĐỘNG / RESTART

```powershell
# Server 7777 (restart khi sửa server.py)
Get-Process python | Where-Object { $_.CommandLine -like '*uvicorn*app.server*' } | Stop-Process -Force
cd D:\TNT_AI\venture_foundry\media
.venv\Scripts\python.exe -m uvicorn app.server:app --host 127.0.0.1 --port 7777

# Desktop app
.venv\Scripts\python.exe desktop_app/app.py

# Chrome CDP cho Flow
.venv\Scripts\python.exe tools/launch_flow_chrome.py
```

## 7. LƯU Ý TOOLING

- JSON escape `\\t` khi write_file → file có tab thật, cần đọc lại verify
- PowerShell dùng `;` không dùng `&&`
- `write_file` đôi khi ghi 0 bytes — retry
- `run_python` phá indent block lồng — dùng list comprehension hoặc helper
- Console cp1252 không in tiếng Việt — dùng `-X utf8` hoặc `io.TextIOWrapper`
- File `__file__`, `__init__`, `__name__` bị strip → dùng `chr(95)` hoặc đọc verify ngay
- DETACHED_PROCESS (0x8) phá network → chỉ dùng CREATE_NEW_PROCESS_GROUP (0x200)

## 8. VIDEO OUTPUT ĐÃ TẠO (verify)

- `output/pipeline_flow_v2.mp4` (6.5 MB, flow OK)
- `output/pipeline_flow_v3.mp4` (7.7 MB)
- `output/FINAL_v2.mp4` (8.6 MB, compose + boost score 100)
- `output/chMialinhcuteai_anime_054e2d220b20261015_182453.mp4` (7.6 MB, job thật qua runner, fallback Pexels)

## 9. CÂU HỎI MỞ

- Caption fix có thực sự hoạt động trong video output cuối không? (chưa chạy end-to-end)
- Do_run() UI đã gửi modules dict chính xác chưa? (cần test thật)
- Module rác nào an toàn để xóa? (cần list chi tiết)
- Auto-delete tiêu chí? (chưa có)
