# KE HOACH NOI NHANH A VAO NHANH B
Ngay: 2026-09-21

## KET QUA USER MUON
He thong tu dang video MOI deu dan, dung noi dung that, co phan tich trend, khong dung worker gia.

## HIEN TRANG (da khao sat code)
- ops/scheduler_tick.py (23 dong): tao bang schedule, chen job kind='publish' status='queued' vao bang jobs. KHONG goi auto_publish.
- ops/worker.py (26 dong): doc job queued, TAO DECISION GIA (topic random tu list cung TP, format random), tao video 'queued_render'. KHONG goi auto_publish.
- ops/auto_publish.py (87 dong): entry THAT, ham run(topic=None,target_dur=14.0,force=False,...). Tu chon topic neu khong truyen.
- ops/autopublish_runner.py (49 dong): CAU NOI THAT, main() kiem tra cooldown (TNT_PUB_COOLDOWN=10800) roi goi auto_publish.run(target_dur=14.0). Day la ham worker NEN goi.

## KET LUAN
Cau noi da co san (autopublish_runner.main). Viec chinh la: cho worker.py goi autopublish_runner.main() thay vi tao decision gia.

## 4 VIEC THEO HANDOFF + UU TIEN REQUIREMENTS
1. [YC1] worker.py goi autopublish_runner.main() thay vi tao decision gia <-- RUI RO THAP, GIA TRI CAO
2. [YC1] scheduler_tick.py giu nguyen (no chi xep job); worker lo phan publish that
3. [YC3] Noi trend_scan vao decision engine (trend_scan.py chi 125 byte - can xem)
4. [YC2] Them idea generator Gemini free (chua co)

## RUI RO
- worker.py hien tao decision gia -> neu doi sang publish that, MOI lan worker chay se DANG VIDEO THAT (ton quota YouTube).
- Cooldown 3h da co trong autopublish_runner -> an toan phan nao.
- Can backup worker.py truoc khi sua.

## DE XUAT
Buoc 1 (an toan, lam ngay): backup worker.py -> worker.py_bak, sua worker.py goi autopublish_runner.main().
Buoc 2: test 1 lan voi cooldown, kiem tra log autopublish.log.
Buoc 3: do trend that vao decision.

## CHO USER XAC NHAN
Sua worker.py de DANG THAT ngay bay gio hay chi o muc 'tao decision that' (chua dang)?
