# HANDOFF - TNT Media OS
Cap nhat: 2026-09-22 (phien 4). DOC FILE NAY TRUOC, KHONG DOC GI KHAC.

=========================================================
## 0. CHAY NGAY (neu chi co 30 giay)
=========================================================
python ops/state.py latest
python ops/state_sync.py

=========================================================
## 1. HE THONG CO GI
=========================================================
Nhanh A - PUBLISH THAT: _serve.py -> ops/control_center.app -> channel_producer.run_many -> os_publish.publish
Ledger: memory/tnt_media.db (videos=255 / publishes=235)

=========================================================
## 2. 7 YEU CAU - TRANG THAI (tat ca XONG)
=========================================================
YC1 XONG: ops/scheduler_cc.py (cron moi kenh).
YC2 XONG: ops/idea_generator.py (Groq) + content_db rieng.
YC3 XONG: ops/trend_scan.py (170 trend).
YC4 XONG: ops/weights_tuner.py + decision_engine dung weights.
YC5 XONG (artifacts): deploy/oracle_setup.sh + systemd + README_ORACLE.md.
YC6 XONG: ops/evolution.py (3 cap: A/B, weights, tool gen).
YC7 XONG: ops/os_api.py (quota per channel) + /api/quotas.

=========================================================
## 3. VIEC TIEP THEO (neu can)
=========================================================
1. [YC5] Tao VM Oracle + scp code + sudo bash deploy/oracle_setup.sh
2. YC6: dat cron chay ops/evolution.py hang tuan
3. YC4: dat cron chay ops/weights_tuner.py hang ngay
4. Mo rong dashboard.html hien thi /api/quotas

=========================================================
## 4. LENH/TOOL CO SAN
=========================================================
ops/scheduler_cc.py - YC1 cron scheduler
ops/weights_tuner.py - YC4 weights tu analytics
ops/decision_engine.py - YC4 decision + weights
ops/evolution.py - YC6 evolution 3 cap
ops/os_api.py - YC7 quota per channel
ops/channel_producer.py - pipeline build+publish per kenh
deploy/oracle_setup.sh - YC5 bootstrap Oracle VM

=========================================================
## 5. CANH BAO
- Gemini key 402. Groq dung openai/gpt-oss-120b, phai co User-Agent.
- Moi kenh topics rieng trong channels/<name>.json. KHONG dung chung.
- Terminal timeout 60s -> chay detached + poll.
- Agent transport an space dau dong + an * va __ -> dung chr(32)/chr(9)/chr(95).
