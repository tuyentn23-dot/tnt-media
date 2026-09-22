# 7 YEU CAU GOC CUA USER

Day la 7 yeu cau bat buoc. Moi quyet dinh ky thuat phai phuc vu it nhat 1 yeu cau.

## YC1 - Dang tu dong deu dan
Trang thai: XONG
Da co: ops/scheduler_cc.py (cron 5 truong, doc scheduleCron tung kenh, chay channel_producer.run_many), ops/autopublish_runner.py da noi decision B.
Cron: Mialinhcute 0 9,15,21 * * *; vilevi5676 0 8,12,18,21 * * *

## YC2 - Noi dung MOI hoan toan
Trang thai: XONG
Da co: ops/idea_generator.py (Groq), channels/<cid>/content_db.json rieng tung kenh, loc hook da publish.

## YC3 - Trend tai thoi diem dang
Trang thai: XONG
Da co: ops/trend_scan.py (Google Suggest free, 170 trend).

## YC4 - Chon cach viral cao nhat
Trang thai: XONG
Da co: ops/weights_tuner.py (hoc tu memory/tnt_media.db metrics -> channels.weightsJson), ops/decision_engine.py dung weights khi cham diem topic/format/hour.

## YC5 - Dang duoc DU MAY TINH TAT
Trang thai: XONG (artifacts san sang deploy)
Da co: deploy/oracle_setup.sh, deploy/tnt-scheduler.service, deploy/tnt-dashboard.service, deploy/README_ORACLE.md (Oracle Always-Free ARM).
Buoc cuoi: tao VM + scp code + chay bootstrap (xem README).

## YC6 - Tu nang cap (evolution loop 3 cap)
Trang thai: XONG
Da co: ops/evolution.py - cap1 A/B prompt (experiments), cap2 weights tuning (weights_tuner), cap3 tool gen + approve (memory/gen_tools).

## YC7 - Nhieu kenh (dashboard + quota)
Trang thai: XONG
Da co: ops/os_api.py (quotas per channel: topics, tokenPath, voice, quota, used24h, remaining), moc vao control_center /api/quotas + /api/os/state.

## RANG BUOC
- Mien phi truoc, tra phi sau khi thay hieu qua
- Khong sua TNT AI core, gateway, overlay, Monolux, Trader, PickleballOS
- Moi file trong venture_foundry/media/
