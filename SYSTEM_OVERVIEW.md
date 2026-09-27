# SYSTEM OVERVIEW - TNT Media OS

> Doc file nay DAU TIEN moi phien.
> Sau do: STATE.md, PHIEN_HANDOFF.md, PIPELINE_SPEC.md

## 1. HE THONG LA GI

TNT Media = he thong tu dong san xuat + dang video YouTube 2 kenh:
- Mialinhcute: kids + gacha/anime, 9:16, ~20s
- vilevi5676: facts/khoa hoc/lifestyle + nguoi noi tieng, 9:16, ~90s

## 2. KIEN TRUC 3 TANG

CONTROL: Tray icon -> Web UI (port 7777) -> API -> DB
DATA: pipeline runner -> modules/ -> publish -> state/pipeline.db
DEV: agent chi sua ops/ + app/ui/

Nguyen tac: Control khong goi module, Data khong tu quyet, Dev khong tu dang.

## 3. CAY THU MUC

media/
 pipeline/ HARD - cam sua (state, runner, job, scheduler, selfcheck)
 ops/ LOGIC (agent lam viec):
 content_crawler.py [MOI] Crawl RSS 413 items/lan
 live_content.py [MOI] RSS -> video item
 voice_engine.py [MOI] 6 voices + 4 presets
 channel_loader.py load content (static + live)
 channel_style.py render HD 1080x1920
 content_video5.py scene + TTS
 os_publish.py upload YouTube
 quality_gate.py kiem tra 1080x1920
 app/
 server.py FastAPI :7777
 tray.py tray + auto-spawn
 ui/index.html 13 tabs UI
 state/pipeline.db SQLite - NGUON SU THAT
 channels/ content db per kenh
 logs/ output/

## 4. DATABASE 9 BANG

channels, jobs, publications, topics, assets, audit, quota, modules_ver, trends

Status publication: rendered -> approved -> published | publish_failed

## 5. FLOW CHAY VIDEO

1. Web UI -> Job Builder -> Create + Run
2. POST /api/jobs -> tao job (pending)
3. POST /api/jobs/{id}/run -> spawn runner
4. runner: load content -> dedup -> build styled -> ghi publication
5. Web UI Approval -> Approve
6. Web UI Publications -> Publish -> YouTube

## 6. CHAY HE THONG

Khoi dong: chay VBS trong Startup folder (TNT_Media_OS_v2.vbs)
Sau 8s: tray icon, server port 7777, Edge app window.
UI: http://127.0.0.1:7777/ui/index.html
Kill: taskkill /F /IM pythonw.exe ; taskkill /F /IM ffmpeg.exe
Test: python -m pipeline.selfcheck (25 PASS / 0 FAIL)

## 7. API ENDPOINTS

Read:
 GET /api/health channels publications jobs pending
 GET /api/topics trends assets/list analytics/quota scheduler/status
 GET /api/diagnostics/logs/list

Write:
 POST /api/jobs tao job
 POST /api/jobs/{id}/run chay ngay
 POST /api/jobs/{id}/schedule hen gio
 DELETE /api/jobs/{id} xoa
 POST /api/publications/{id}/publish approve reject
 POST /api/cleanup backup killswitch

## 8. CHANNELS

Mialinhcute: anime, roblox, cute_animals, gacha, meme | hong vang | 20s
vilevi5676: news, world, facts, sci, ent, lifestyle, food, animals,
 curiosity, whatif, nostalgia | xanh cam | 90s
 UU TIEN: nguoi noi tieng (ca sy, showbiz, lanh tu, vi nhan)

## 9. WORKAROUND MOI TRUONG

Tool 2026-09 bi mangle nang:
- Strip dau sao va dunder (gach duoi kep)
- Mangle backslash + quotes long nhau
- Vo triple-quote
- Strip dunder name thanh name

Cach ghi file dang tin (list join):
 U = chr(95); NL = chr(10); T = chr(9)
 L = []
 L.append(chr(39) + import os + chr(39))
 L.append(T + chr(39) + return 1 + chr(39))
 content = NL.join(L) + NL
 open(out.py, w, encoding=utf-8).write(content)
 import ast; ast.parse(content)

Ky tu dac biet:
 dau sao = chr(42), gach duoi = chr(95), backtick = chr(96)
 dquote = chr(34), squote = chr(39)
 TAB = chr(9), newline = chr(10), backslash = chr(92)

File lon: base64 encode -> save -> decode ghi lai

## 10. QUY TAC CHO PHIEN AGENT

KHONG:
- Sua pipeline/ (HARD)
- Sua schema state/pipeline.db
- Tu dang video (chi user bam Publish)
- Xoa channels content db

DUOC:
- Sua ops/ + app/ui/
- Them module, RSS source, voice, preset

Checklist moi phien:
1. Doc SYSTEM_OVERVIEW.md (file nay)
2. Doc STATE.md + PHIEN_HANDOFF.md
3. Query DB de biet trang thai
4. Lam 1 task
5. Test: python -m pipeline.selfcheck
6. Viet PHIEN_HANDOFF.md cho phien sau

## 11. TROUBLESHOOTING

ffmpeg crash 0xc0000142 -> DETACHED -> CREATE_NO_WINDOW
Popup cmd nhay len -> import ops._no_window truoc
Video 720p < 1080p -> sua channel_style + content_video5
Publish fail khong bao -> check res.get(ok)
Cooldown chan topic -> dung topic unique
Content trung -> dung live RSS
Giong don dieu -> dung voice_engine.tts
Video dung dot ngot -> TODO: them outro fade

## 12. LIEN KET

- PIPELINE_SPEC.md - Kien truc + schema
- AGENT_RULES.md - Quy tac cho phien
- STATE.md - Trang thai hien tai
- CHANGELOG.md - Lich su thay doi
- PHIEN_HANDOFF.md - Handoff moi nhat

Phien truoc da xong: Task 1 (Content live RSS) + Task 2 (Voice diversity).
Phien sau can lam: Task 3 (Khong dung dot ngot) + Test E2E.
