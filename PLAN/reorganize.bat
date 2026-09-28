@echo off
REM ============================================================
REM TNT MEDIA OS - Tai cau truc PLAN/DEV/RUN (CHAY KHI APP DA DUNG)
REM ============================================================
REM CANH BAO: Script nay DI CHUYEN file. Hay BACKUP workspace truoc.
REM Yeu cau: da dung tray/server/scheduler/moi python.exe cua app.
REM ============================================================
setlocal
cd /d %~dp0..
set ROOT=%CD%
echo ROOT=%ROOT%

REM --- Kiem tra khong con python.exe cua app ---
tasklist /fi "imagename eq python.exe" | findstr /i python.exe >nul
if %errorlevel%==0 (
 echo [STOP] Con python.exe dang chay. Hay dung het truoc khi chay script nay.
 pause
 exit /b 1
)

REM --- Backup DB ---
if not exist RUNstate mkdir RUNstate
if exist statepipeline.db (
 echo [1] Backup DB...
 if not exist RUNbackups mkdir RUNbackups
 copy /Y statepipeline.db RUNbackupspipeline_pre_migrate.db
)

REM --- Giai doan 1: RUNTIME -> RUN ---
echo [2] Di chuyen runtime -> RUN...
for %%D in (state output logs backups work cloud_media library music_bank movies memory) do (
 if exist "%%D" (
 if not exist "RUN%%D" (
 move "%%D" "RUN%%D"
 if exist "RUN%%D" mklink /J "%%D" "RUN%%D"
 )
 )
)

REM --- Giai doan 3: DOCS -> PLAN ---
echo [3] Di chuyen tai lieu -> PLANdocs...
if not exist PLANdocs mkdir PLANdocs

REM --- Giai doan 2: SOURCE -> DEV (LAM SAU, CAN SUA sys.path) ---
echo [4] Source: xem PLANMIGRATION_PLAN.md giai doan 2 (chua tu dong).

echo.
echo [DONE] Runtime da vao RUN (kem junction). Source giu nguyen.
echo Tiep theo: sua paths.py, chay test, roi moi chuyen source.
pause
endlocal
