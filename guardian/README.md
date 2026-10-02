# GUARDIAN - He thong bao ve TNT Media OS

Muc dich: ngan chan xoa/sua nham file quan trong, bao toan he thong.

## Nguyen tac bat buoc cho MOI AI agent

1. TRUOC khi lam gi: chay snapshot
 python guardian/guard.py before

2. SAU khi lam xong: verify
 python guardian/guard.py verify

3. KHONG BAO GIO dung os.remove truc tiep tren file quan trong.
 Dung: python guardian/safe_fs.py remove <file>
 (file se duoc chuyen vao _trash/archive, co the restore)

4. KHONG dung lenh xoa hang loat (Remove-Item, rm -rf, del).
 Dung: python guardian/safe_fs.py remove ...

5. Neu file quan trong bi mat, khoi phuc:
 python guardian/snapshot.py restore

## File quan trong (critical.json)

Gom 4 nhom: ops_core, app, root, config. Xem chi tiet trong guardian/critical.json.
Neu them module moi quan trong, cap nhat critical.json.

## Cac lenh

python guardian/guard.py before # snapshot truoc khi lam
python guardian/guard.py verify # kiem tra sau khi lam
python guardian/snapshot.py snapshot # snapshot thu cong
python guardian/snapshot.py verify # kiem tra file quan trong
python guardian/snapshot.py restore # khoi phuc tu snapshot moi nhat
python guardian/safe_fs.py list # liet ke archive
python guardian/safe_fs.py remove X # xoa an toan (archive X)
python guardian/safe_fs.py restore TS # khoi phuc tu archive TS

## Git pre-commit hook

Da cai .git/hooks/pre-commit: tu dong verify truoc khi commit.
Neu file quan trong mat, commit se bi chan.

