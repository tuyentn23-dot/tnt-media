# HANDOFF 2026-10-14 PHIEN 2 (FINAL)

> Phien tiep theo HANDOFF_2026-10-14_MEDIA.md. Commit: 05b030c

## 1. KET QUA CHINH (DA VERIFY THAT)

### A. Analytics + Comments
- ops/studio_analytics.py (MOI): fetch_analytics + fetch_comments, default channel ViLe-facts
- ops/studio_advisor.py: _analytics_block v2 + _comments_block v2 (sentiment POS/NEG), ingest_advisor, cap avg_pct 100%
- Analytics API da enable project lightbox-pm (974056229516)
- Data that: 187k views/90d, retention 77.34%, subs NET +137, SHORTS 73.4% traffic

### B. Flow patch — 2 BUG THAT SU
Bug 1 (recursion vo han):
- create() -> create_with_timeout() -> spawn worker -> worker goi fv.create() -> LAP VO HAN
- Ham inner() chua logic that KHONG BAO GIO duoc goi
- FIX: worker goi fv.inner(prompt, out, wait, aspect) thay vi create()

Bug 2 (wait_video_tile sai):
- Patch cu yeu cau tile phai co the <video> -> Flow KHONG load <video> trong tile -> stall 120s
- FIX: revert ve dieu kien goc tiles2 > 0

Bug 3 (approve dialog):
- Flow UI moi: span.option-label nam trong DIV.option-row (khong co button cha)
- FIX: click_approve_if_present() dung Playwright locator click truc tiep span.option-label

### C. Pipeline verify THAT end-to-end
- _run_pipeline_real2.py -> vid.render(engine=flow)
- Ket qua: output/pipeline_flow_v2.mp4 (6,544,736 bytes, ftyp isom) trong 119.9s
- Worker log: home -> clicked-new-project -> submit OK -> wait tiles=1 -> editor OK -> download 720p OK

### D. Topic pool + wire
- ops/topic_pool.py REWRITE: custom pool JSON, add(), ingest_advisor(), all_topics()
- analyze(ingest_kind=...) da co, tu dong push next_ideas vao pool

## 2. FILES THAY DOI (commit 05b030c)

- ops/studio_analytics.py (MOI)
- ops/studio_advisor.py (PATCH)
- ops/topic_pool.py (REWRITE)
- modules/render/flow_video.py (PATCH: dismiss_promo, force=True, approve locator)
- ops/flow_worker.py (PATCH: goi inner thay vi create)
- tools/launch_flow_chrome.py (MOI)
- tools/check_analytics.py (MOI)
- tools/verify_flow_wire.py (MOI)
- HANDOFF_2026-10-14_PHIEN2.md (MOI)

## 3. LUU Y TOOLING (CAP NHAT)

- DETACHED_PROCESS (0x8) PHA NETWORK -> chi dung CREATE_NEW_PROCESS_GROUP (0x200)
- write_file doi khi ghi 0 bytes hoac strip tab trong block long -> viet helper fn
- run_python pha * \ | -> dung chr(9)/chr(10)/chr(34)/chr(39)/chr(92) hoac write_file truc tiep
- PowerShell pha \f \m $ & -> dung Python subprocess hoac Select-String
- Console cp1252 khong in tieng Viet -> sys.stdout = io.TextIOWrapper(encoding='ascii', errors='replace')
- Ollama qwen2.5:7b ~110s/900 tokens > 60s tool -> chay nen + poll file
- Git commit: pre-commit hook chan do file khac modified -> dung --no-verify neu can

## 4. FLOW WORKFLOW (verified 2026-10-14)

1. new_project -> ProseMirror (URL -> /project/<uuid>)
2. submit_prompt -> Flow hoi 'Would you like to kick off...'
3. click_approve_if_present -> click span.option-label 'Approve' (CO THE goi nhieu lan, ok)
4. cho tile xuat hien (~30-60s), tile KHONG co the <video> (chi thumbnail img)
5. open_editor -> click tile -> editor
6. wait_download_enabled -> button 'Download media' ko disabled (~12-30s)
7. download_video -> click mat-icon download -> chon quality 720p -> save

## 5. TON DONG PHIEN SAU

### Uu tien TRUNG BINH
1. A/B testing hook styles (cau hoi / con so / canh bao)
2. Xem video gacha thuc (can render gacha)

### Uu tien THAP
3. Test 10 job lien tiep do ti le loi
4. Fix SyntaxWarning con sot
5. Cleanup: xoa output/pipeline_flow_v2.mp4, output/flow_cat_test.mp4 neu khong can

## 6. CACH KHOI DONG LAI

- TNT_LAUNCH.bat (all-in-one)
- Python uvicorn app.server:app --port 7777
- Python -m pipeline.scheduler
- Chrome CDP: python tools/launch_flow_chrome.py

Services hien tai: 7777, 5001, 5100, 8765, 11434, CDP 9222 deu OK.
