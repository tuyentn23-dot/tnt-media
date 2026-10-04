# AGENT_RULES - Quy tac bat buoc cho AI agent

## BUOC 0 - BAT BUOC DAU TIEN

DOC FILE BOOTSTRAP.md TRUOC KHI LAM BAT CU DIEU GI.

Sau do chay:


python -m guardian.agent_boot


Lenh nay in ra:
- Kien truc he thong (pipeline/modules/app/state/guardian)
- Trang thai DB + git
- Danh sach critical file CAM SUA
- Modules hien co (agent lam viec o day)
- Tai lieu phai doc

## TRUOC KHI LAM

1. Doc BOOTSTRAP.md (file goc)
2. Doc STATE.md + CHANGELOG.md + PIPELINE_SPEC.md
3. Chay: python guardian/guard.py before (snapshot)

## TRONG KHI LAM

- KHONG dung os.remove / Remove-Item / rm truc tiep
- Xoa file: python guardian/safe_fs.py remove <file>
- Khong xoa hang loat (glob + remove)
- Dung absolute path hoac cd dung workspace
- Kiem tra git status truoc khi thao tac file
- KHONG SUA: pipeline/, state/pipeline.db, guardian/, app/server.py
- CHI SUA: modules/, ops/ (neu can thiet)

## SAU KHI LAM XONG

1. Chay: python guardian/guard.py verify
2. Chay: python -m pipeline.selfcheck
3. Chay: python -m pytest tests/ -q

Ca 3 PHAI PASS.

## 4 YEU CAU 100% BAT BUOC

1. NHO MOI LAN - chay agent_boot dau phien, cap nhat CHANGELOG.md cuoi phien
2. KHONG SAI - chay tests/ truoc commit, selfcheck sau khi sua
3. KHONG PHA CAI DA LAM - khong sua pipeline/, state/pipeline.db, guardian/
4. 100% DAM BAO - checklist trong BOOTSTRAP.md muc 8 phai dat het
