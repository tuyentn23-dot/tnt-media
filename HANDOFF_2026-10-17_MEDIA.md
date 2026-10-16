# HANDOFF 2026-10-17 — TNT MEDIA (sync fix + viral research + UI redesign)

> Session: 2026-10-17. Commit: 4b27321 (28 files, +1707/-175)

## 1. TRẠNG THÁI HỆ THỐNG

- Server 7777: OK (305 pubs, 318 jobs)
- Scheduler: alive (heartbeat 30s)
- Desktop app: chạy (UI redesign)
- Chrome CDP 9222: OK
- Groq API: OK (qwen/qwen3.8-27b, tiếng Việt tốt)
- Ollama 11434: OK (fallback)

## 2. FIX CHÍNH

### Đồng bộ hình + caption + tiếng
- compose.py: thay tpad=stop_mode=clone bằng setpts=factorPTS (stretch video khớp voice)
- step_mux: vdur=min(vd,voiced) — hình+tiếng kết thúc cùng lúc
- caption_engine: cắt caption theo câu qua flag is_end

### Recovery
- recovery.py: 300s -> 1800s stale threshold
- runner.py: heartbeat 60s -> 30s

### Nút Đăng
- widgets.py: busy_wrap(parent,fn,msg) đúng signature
- api.py: publish timeout 3s -> 600s, bulk 1800s, run_job 900s

## 3. FEATURES MỚI

- ops/viral_research/: YouTube Shorts (≤180s) + pattern analysis + 4 API
- ops/music_index.py: 9 mood × 221 files, pick theo content+job_id
- ops/auto_cleanup.py: xoá video đã publish >14d hoặc output >2GB
- providers/free_llm.py: Groq qwen3.8-27b / Gemini / OpenRouter / Mistral
- ai_content: Groq primary (1.8s vs 56s Ollama), max_tokens 1200-1500
- trend_analyzer: score recency+niche+length+source, YouTube per-niche
- vn_guard: reject chỉ khi d==0 hoặc >70% bad words
- UI: caption/music-only checkbox, viral button, topic full-width

## 4. ƯU TIÊN PHIÊN SAU

Cao:
1. Verify publish qua UI (click nút Đăng thật)
2. Verify music-only mode (checkbox → không caption)
3. Test job với music_only=True

Trung bình:
4. studio_advisor dùng viral_ref đã inject
5. TikTok/IG bị chặn yt-dlp — cần Playwright nếu muốn
6. UI polish

Thấp:
7. Xoá 8 file .bak_before_syntax_repair_20260906
8. Check auto_cleanup trigger

## 5. TOOLING WARNINGS

- Tool strip __: dùng chr(95)2 hoặc FKEY pattern
- Tool strip _ prefix: TRÁNH glob _.py (dễ xóa file gốc)
- Tool strip : dùng xx thay x**2
- Tool strip indent: dùng base64 encode
- Tool output ~350 ký tự: đọc chunk 5-10 dòng

## 6. FILE QUAN TRỌNG

- compose.py, caption_engine.py, voice_synth.py, vn_guard.py
- ai_content.py, viral_research/, music_index.py, auto_cleanup.py
- providers/free_llm.py
- pipeline/runner.py, recovery.py
- app/server.py
- desktop_app/api.py, widgets.py, views/pipeline.py

## 7. CÁCH RESTART


Get-Process pythonw | Stop-Process -Force
cd D:\TNT_AIenture_foundry\media
.venv\Scripts\pythonw.exe -m pipeline.scheduler &
.venv\Scripts\pythonw.exe app/server.py &
.venv\Scripts\pythonw.exe desktop_app/app.py &


## 8. CÂU HỎI MỞ

- Publish timeout 600s đủ?
- Music-only test end-to-end?
- Groq 30 RPM đủ? (4 kinds × 2 items = 8 calls, OK)
- vn_guard >70% có chặt quá?
- TikTok/IG cần Playwright?
