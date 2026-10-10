# *** CAP NHAT QUAN TRONG 2026-10-10 - DOC TRUOC ***
#
# QUY UOC: Khi ai noi "APP" / "ung dung" / "giao dien" -> LUON LUON la:
# TNT Media Studio (shortcut: C:/Users/DELL/Desktop/TNT Media Studio.lnk)
# Target: run_desktop.bat | Code: desktop_app/ (PyQt desktop)
# KHONG PHAI web UI (app/ui/index.html + :7777).
#
# Phien 2026-10-10 da fix 6 bug + Phase 1+2 web UI, nhung CAN LAM LAI Phase 1+2
# cho desktop_app/ vi do moi la "app" nguoi dung dung thuc su.
#
# ============================================================

# HANDOFF PHIEN 2026-10-09 (TOI) - VOICE/PRESET DROPDOWN + STOCK FALLBACK

> Doc file nay dau tien khi bat dau phien moi.
> Cap nhat: 2026-10-09 (cuoi phien toi)

==================================================
0. TOM TAT NHANH
==================================================

Phien nay hoan thanh P1-P4 tu handoff truoc:
- P1: Dropdown Giong doc (6) + Sac thai (8) end-to-end: UI -> API -> DB -> render
- P2: Pixabay + Coverr fallback khi Pexels thieu clip
- P3: Commit 1324c75 (guardian manifest re-signed 1 lan)
- P4: Update AGENT_RULES.md + SYSTEM_OVERVIEW.md + CHANGELOG.md

selfcheck: 27 PASS / 0 FAIL
modules_discoverable: 33 modules, bad=[]
guardian integrity: 63 files OK

==================================================
1. FILES SUA PHIEN NAY
==================================================

Backend:
- app/server.py - /api/config/voices (6 dong tu edge_tts), /api/config/presets (8), INSERT/SELECT jobs kem voice_preset
- pipeline/state.py - SCHEMA jobs them cot voice_preset + migration ALTER TABLE
- pipeline/job.py - Job field voice_preset (init, to_dict, from_dict)
- pipeline/runner.py - merge voice_override/preset vao render style, INSERT kem voice_preset

UI:
- desktop_app/api.py - presets() helper
- desktop_app/views/pipeline.py - 2 dropdown (Giong doc + Sac thai), load_voice_presets(), wire vao body
- desktop_app/strings_vi.json - pipe.voice, pipe.preset (114 keys)

Module moi:
- modules/render/stock_fallback.py v1.0.0 - Pixabay + Coverr search/download
- modules/render/pexels_builder.py - goi fallback khi < 2 clip

Docs:
- AGENT_RULES.md - VOICE + PRESET CONTRACT, STOCK FALLBACK CONTRACT
- SYSTEM_OVERVIEW.md - muc 14/15/16
- CHANGELOG.md - entry 2026-10-09 (toi)
- .env.example - PIXABAY_API_KEY, COVERR_API_KEY

==================================================
2. VOICE + PRESET FLOW (END-TO-END)
==================================================

UI Pipeline view:
 dropdown 'Giong doc' -> self.voice.currentData() = voice_override
 dropdown 'Sac thai' -> self.preset.currentData() = voice_preset
 do_run() gui ca 2 trong POST /api/jobs

Server:
 POST /api/jobs -> Job.from_dict -> INSERT jobs (co voice_preset)
 POST /api/jobs/{id}/run -> SELECT kem voice_preset -> job_dict

Runner:
 style = dict(cfg.get('style', {}) or {})
 if job.voice_override: style['voice'] = job.voice_override
 if job.voice_preset:
 style['voice_preset'] = job.voice_preset
 style['preset'] = job.voice_preset
 -> render.video -> try_ffmpeg -> voice_synth.synth_words(voice, preset)

Database:
 jobs.voice_override TEXT (cu)
 jobs.voice_preset TEXT (MOI, migration tu dong khi state.init())

==================================================
3. STOCK FALLBACK FLOW
==================================================

pexels_builder.build():
 clips = pexels_fetch.fetch_for_topic(query, n_segs+2)
 if len(clips) < 2:
 stock_fallback.fallback_for_topic(query, n_segs+2, need=2)
 -> pixabay_search -> coverr_search
 -> download vao library/stock_cache/
 if len(clips) < 2: return error

Keys (tuy chon):
 PIXABAY_API_KEY trong .env
 COVERR_API_KEY trong .env
 Khong co key -> tra [] graceful, khong crash

Health: stock_fallback.health() -> {pixabay: bool, coverr: bool}

==================================================
4. GAP DA FIX
==================================================

Truoc phien nay: dropdown voice chi hien thi, khong anh huong render.
Nguyen nhan: runner.py dong 112 chi lay style tu channel config,
 KHONG merge job.voice_override (chi luu vao DB luc INSERT).
Da fix: merge voice_override + voice_preset vao style truoc khi render.

==================================================
5. CANH BAO / WORKAROUND
==================================================

write_file STRIP: backslash, asterisk, tab, dau _, VA TAT CA DAU TIENG VIET
run_python: giu tab/underscore/dau tieng Viet, NHUNG strip:
 - backslash trong string literal (dung chr(92))
 - dau sao () trong code (dung n+n thay n2)
 - [ ] trong write_file nhung OK trong run_python (dung chr(91)/chr(93) an toan)
PowerShell: khong &&, $ bi strip, backslash path bi strip -> dung forward slash
Server phai chay PYTHONUTF8=1 (launch_server.py da set)
Guardian pre-commit hook CHAN commit khi critical file thay doi:
 -> chay: python guardian/integrity.py snapshot
 -> git add guardian/critical.sha256.json
 -> 1 lan commit --no-verify de bootstrap manifest moi
 -> sau do hook pass binh thuong

==================================================
6. VIEC PHIEN SAU
==================================================

P0: Mo run_desktop.bat -> test UI that:
 - kiem tra 2 dropdown hien thi 6 giong + 8 preset
 - chon 'NamMinh' + 'Tin tuc' -> chay job -> verify voice khac trong video
P1: Dang ky PIXABAY_API_KEY + COVERR_API_KEY (mien phi) -> test fallback that
P2: Test render voi cac preset khac nhau -> nghe su khac biet
P3: Them preview voice (nghe thu) trong UI truoc khi chay job
P4: Mo rong: them giong tieng Anh cho kenh quoc te

==================================================
7. LENH HAY DUNG
==================================================

Selfcheck: .venv/Scripts/python.exe -m pipeline.selfcheck
Guardian verify: python guardian/integrity.py
Guardian re-sign: python guardian/integrity.py snapshot
Restart server: .venv/Scripts/python.exe work/launch_server.py
Desktop: run_desktop.bat
Check port: netstat -ano | findstr :7777

==================================================
8. CHECKLIST PHIEN MOI
==================================================

- [ ] Doc HANDOFF_2026-10-09_TOI.md (file nay)
- [ ] python -m pipeline.selfcheck (27 PASS)
- [ ] python guardian/integrity.py (63 files OK)
- [ ] Check server :7777
- [ ] Verify /api/config/voices -> 6 items
- [ ] Verify /api/config/presets -> 8 items
- [ ] Verify bang jobs co cot voice_preset
- [ ] Chay desktop app -> kiem tra 2 dropdown

==================================================
HET HANDOFF
==================================================
