# HANDOFF BO SUNG - 2026-09-27 (phien 2)

## Muc tieu phien: duyet PLAN/DEV/RUN + fix cua so cmd den chop tat khi render/publish

## 1. FIX CUA SO CMD DEN (render/publish)
- NGUYEN NHAN GOC: ops/_no_window.py BI THIEU (chi con trong _archive_tmp_20260927).
 => app/server.py, app/tray.py, pipeline/runner.py import that bai IM LANG (try/except pass).
 => Moi subprocess.Popen spawn ffmpeg/edge hien cua so cmd den + chop tat.
- FIX 1 (d2c68ea): khoi phuc ops/_no_window.py (monkeypatch subprocess.Popen toan cuc, CREATE_NO_WINDOW=0x08000000 + STARTF_USESHOWWINDOW/SW_HIDE).
- FIX 2 (a7dfecc): nang cap _no_window.py patch CA os.system (nhieu file render dung os.system, bypass Popen).
 + tao ops/no_window.py (shim tuong thich ten cu: runner.py import from ops import no_window).
 + tao ops/init.py: tu dong ap patch cho MOI import ops (bao hiem toan dien).
- BANG CHUNG:
 * import ops._no_window OK / ops.no_window OK / ops OK
 * subprocess.Popen.name == _NWPopen (da patch)
 * Popen_patched=True, system_auto_patched=True
 * p0_check 21/21 PASS, selfcheck 27/27 PASS
- CHUA XAC MINH: hanh vi truc quan tren Windows (cua so cmd khong hien) can ban chay tay 1 job render de xac nhan.

## 2. PLAN/DEV/RUN
- Da DUYET luat: PLAN/rules/ARCHITECTURE.md, DEV/rules/, RUN/rules/.
- CHUA di chuyen vat ly thu muc source/runtime vi rui ro cao (import paths).
- Khuyen nghi: thuc hien tai cau truc theo tung buoc nho, co backup, trong phien rieng.

## 3. HEAD
- Truoc phien 2: d6cc7d6
- Sau: a7dfecc
 d2c68ea fix(subprocess): restore missing ops/_no_window.py
 a7dfecc fix(subprocess): global no-window patch via ops/init + shim; also patch os.system

## 4. AN TOAN
- Khong upload YouTube, khong API that, khong sua DB production, khong publish.