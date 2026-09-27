# FILE HONG, TAI LIEU, DU LIEU LECH

## 5. FILE HONG CAN FIX (DA XAC MINH)

### 5.1. ops/channel_style.py - loi indentation dong 39
Bang chung da xac minh: ast.parse bao ERR line 39
Nguy hiem: Van la fallback trong pipeline/runner.py dong 88-89
Sua: Sua file hoac xoa fallback trong runner + xoa file

### 5.2. ops/safe_io.py - loi indentation dong 9
Bang chung da xac minh: ast.parse bao ERR line 9
Sua: Xoa (khong dung o dau)

## 6. TAI LIEU & KIEM THU

### 6.1. Tai lieu lech
- STATE.md: con ghi 540x960, Task 1/2/3 DONE cu
- PHIEN_HANDOFF.md: "All Tasks DONE" cu
- ops/start.py: truy van youtube_url (DA XAC MINH) nhung DB chi co youtube_id

### 6.2. Du lieu lech
- 71 job pending_approval (DA XAC MINH) trong DB
- Trang thai nay KHONG nam trong JOB_TRANSITIONS
- Can doi soat, khong coi la 71 loi
- Lua chon: them pending_approval vao JOB_TRANSITIONS hoac migrate data cu

### 6.3. Selfcheck
File: pipeline/selfcheck.py
- Kiem tra chuoi van ban, co PASS: skip
- Chua chung minh hanh vi
Sua: Viet test hanh vi that (unit + integration + e2e mock)

### 6.4. Git
- Nhieu file cot loi untracked
- Chua co moc khoi phuc day du
Sua: Tao commit hoac tag voi .gitignore dung (khong commit .env, token, media lon)

### 6.5. Modules loader
- Chi kiem tra metadata, chua chung minh interface hoat dong
- Rollback module chua bao phu dependency/config/schema

### 6.6. Evolution
- Tao ban ghi A/B hoac tool stub chua phai cai tien co kiem chung
- Weights tuner chua tach kenh va tuoi video

## 7. KIEM THU CAN BO SUNG

Tao bo test voi tinh huong:
- Video ngan/dai, thieu footage, footage hong
- Khong co mang hoac TTS loi
- Loi dai, ten rieng, caption nhieu dong
- 2 kenh chay gan nhau
- Upload that bai, timeout, thanh cong nhung ghi trang thai loi
- Restart giua job
- Backup va restore
- Bam chay/duyet/dang nhieu lan

Phan biet: unit / integration / e2e mock / kiem chung that.

### Kiem tra chat luong cam nhan
Can xem/nghe video mau. Neu moi truong khong ho tro, bao ro phan chua xac minh.
