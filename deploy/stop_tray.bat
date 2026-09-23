@echo off
powershell -NoProfile -Command "Get-CimInstance Win32_Process | Where-Object { $_.CommandLine -like '*tray_app.py*' } | ForEach-Object { Stop-Process -Id $_.ProcessId -Force }"
echo Tray app stopped.
pause
