# HANDOFF 2026-10-14 PHIEN 2 (FINAL)

> Phien tiep theo HANDOFF_2026-10-14_MEDIA.md. Tat ca muc uu tien CAO da xong + 4/6 muc trung binh.

## 1. DA HOAN THANH

### Analytics + Comments
- ops/studio_analytics.py (MOI): fetch_analytics + fetch_comments, default channel ViLe-facts
- ops/studio_advisor.py: _analytics_block v2 + _comments_block v2, ingest_advisor, cap avg_pct 100%
- Analytics API da enable project lightbox-pm (974056229516)
- Data that: 187k views/90d, retention 77.34%, subs NET +137, SHORTS 73.4% traffic
- Comment sentiment: POS/NEG/NEUTRAL heuristic + tom tat

### Flow fix (MAJOR)
- Root cause worker exit 3: Flow UI moi hien dialog Approve inline (span.option-label trong DIV.option-row, khong co button cha)
- Fix: click_approve_if_present() dung Playwright locator click span truc tiep
- wait_video_tile(): them check <video> trong tile
- Verify end-to-end: output/flow_cat_test.mp4 (3.94 MB, ftyp isom)

### Pipeline wire
- flow_video da wire vao modules/render/video.py (try_flow -> ENGINES)
- Dry-run xac nhan: try_flow duoc goi, prompt build dung, engine=flow uu tien

### Topic pool upgrade
- ops/topic_pool.py REWRITE: custom pool JSON (state/topic_pool_custom.json), add(), ingest_advisor()
- ingest_advisor: doc advisor output -> them next_ideas vao pool (auto infer kind tu channel title)
- analyze(ingest_kind=...) da co param

## 2. FILES THAY DOI

| File | Trang thai |
|---|---|
| ops/studio_analytics.py | MOI |
| ops/studio_advisor.py | PATCH |
| ops/topic_pool.py | REWRITE |
| modules/render/flow_video.py | PATCH |
| tools/launch_flow_chrome.py | MOI (tu _launch_flow_chrome.py) |
| tools/check_analytics.py | MOI (tu _ya_check.py) |
| tools/verify_flow_wire.py | MOI (tu _verify_flow_wire.py) |
| state/topic_pool_custom.json | MOI (auto-gen) |
| output/flow_cat_test.mp4 | MOI (3.94 MB, video test Flow) |

## 3. LUU Y TOOLING QUAN TRONG

- DETACHED_PROCESS (0x8) PHA NETWORK -> chi dung CREATE_NEW_PROCESS_GROUP (0x200)
- write_file doi khi ghi 0 bytes -> retry
- write_file strip tab trong block long -> viet helper fn + early return
- run_python pha indent/backslash/quote -> uu tien write_file, hoac chr(9/10/34/39/92)
- Console cp1252 khong in tieng Viet -> sys.stdout = io.TextIOWrapper(encoding='ascii', errors='replace')
- Ollama qwen2.5:7b ~110s/900 tokens > 60s tool -> chay nen + poll file
- Flow Chrome: chrome.exe --remote-debugging-port=9222 --user-data-dir=flow_chrome_clean (khong dung profile co extension TNT)
- Flow approve: span.option-label 'Approve' hoac 'Always approve' -> locator.click(force=True)

## 4. TON DONG PHIEN SAU

### Uu tien TRUNG BINH
1. A/B testing hook styles (cau hoi / con so / canh bao) — can traffic that
2. Xem video gacha thuc de danh gia tham my

### Uu tien THAP
3. Test 10 job lien tiep do ti le loi
4. Fix SyntaxWarning con sot
5. Xoa output/flow_cat_test.mp4 neu khong can

## 5. CACH KHOI DONG LAI

- TNT_LAUNCH.bat
- Start-Process .venv\Scripts\python.exe -ArgumentList '-m','uvicorn','app.server:app','--port','7777'
- Start-Process .venv\Scripts\python.exe -ArgumentList '-m','pipeline.scheduler'
- Chrome CDP: chay tools/launch_flow_chrome.py

Services hien tai: 7777, 5001, 5100, 8765, 11434 OK. Chrome CDP 9222 OK.
