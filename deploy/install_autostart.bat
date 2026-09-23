@echo off
REM TNT Media OS - autostart installer (run as normal user)
set VBS=D:\TNT_AI\venture_foundry\media\deploy\run_tray.vbs
set STARTUP=%APPDATA%\Microsoft\Windows\Start Menu\Programs\Startup
copy /Y "%VBS%" "%STARTUP%\TNT_Media_OS.vbs"
echo Installed to Startup. Reboot to auto-run.
pause
