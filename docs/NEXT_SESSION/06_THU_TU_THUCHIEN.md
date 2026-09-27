# THU TU THUC HIEN + BANG NGHIEM THU

## THU TU THUC HIEN (KHUYEN NGHI)

1. Bypass quality gate (2.1)
 - Bo force=True trong app/_routes_publish.py dong 38
 - Sua video_health exception trong ops/os_publish.py dong 63-64

2. Chong dang trung (2.3)
 - UPDATE atomic trong _routes_publish.py dong 24-31

3. Temp dir rieng (2.4)
 - tempfile.mkdtemp trong ffmpeg_render.py dong 146, 171

4. Route trung (2.2)
 - Xoa handler cu trong app/server.py dong 219-260

5. Backup API (2.6)
 - Goi ops/backup_state.py trong app/server.py dong 358

6. Tray pause/resume (2.8)
 - File flag state/paused.flag thay vi UPDATE channels

7. Tray cac muc khac (2.9)
 - Trang thai/ Xem loi/ Khoi phuc/ Thoat

8. Giao dien 7777 (2.10)
 - Sua dau nhay, interval, luu config, player xem truoc

9. Scheduler/recovery (3.1, 3.2, 3.3)

10. Fix/xoa file hong (5.1, 5.2)

11. Dong bo tai lieu (6.1, 6.2)
 - STATE.md, PHIEN_HANDOFF.md, ops/start.py
 - Doi soat 71 pending_approval

12. Tao moc Git (6.4)

---

## BANG NGHIEM THU

| Muc tieu | Trang thai |
|---|---|
| Render 1080p | DA XAC NHAN |
| Sua loi job/publish | CO TIEN BO |
| Tray quan ly on dinh | CHUA DAT |
| Giao dien 7777 de dung | CHUA DAT |
| Chong trung + dong thoi | CHUA DAT |
| Caption/hinh/nhac dung | CHUA DAT DAY DU |
| AI nho dung he thong | CHUA DAT |
| Tu tien hoa co kiem chung | CHUA CO |

---

## VIDEO DA PUBLISH PUBLIC (PHIEN TRUOC)

8 video da publish public:

Mialinhcute:
- YluZJfC74VU - Naruto manh nhat khi nao?
- bc7WdiEuqU8 - Meo con lan dau nhin thay tuyet
- M1fz5RCpz3Y - Co gai Gacha bo hoc
- N5-YOlhy0-g - Khi me goi day di hoc

vilevi5676:
- tyjX7YBLXGU - Ca heo tu nhan thuc
- QXSL9dNIC5E - Vi sao bau troi xanh?
- izby5RO5chk - Pho Viet Nam
- FUEuK0JUtL8 - Neu Mat Troi tat

KHONG xoa tru khi co lenh rieng.

---

## LENH THUONG DUNG

- Mo tray: python app/tray.py
- Dashboard: http://127.0.0.1:7777/ui/index.html
- Render: python -m pipeline.runner --channel <id> --kind <kind> [--item-id <id>]
- Dry-run: them --dry-run
- Backup: python ops/backup_state.py --verify
- Recover: python -c "from pipeline import recovery; recovery.recover_stale_jobs()"
- Dump file: python ops/_tmp_dump.py <path> <start> <end>
- Health: python -c "import urllib.request; print(urllib.request.urlopen('http://127.0.0.1:7777/api/health', timeout=5).read())"

---

## NGUYEN TAC LAM VIEC

- KHONG them tinh nang moi khi P0 chua xong
- Sua tung loi, test co y nghia, chi chuyen tiep khi dat
- Moi thay doi schema: migration + backup + test
- Khong nuot loi khong ro ly do
- Log co job_id, video_id, cong doan, phien ban; khong chua bi mat
- Khong hua "khong bao gio hong"; chung minh giam hoi quy bang test
