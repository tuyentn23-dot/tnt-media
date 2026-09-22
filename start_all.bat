@echo off
title TNT Media - Control Center
echo ========================================
echo Starting TNT Media v3
echo ========================================
cd /d D:\TNT_AI\venture_foundry\media
echo Starting API Server on port 8001...
start /min python api_server.py
timeout /t 2 /nobreak > nul
echo Starting Web Server on port 8000...
start /min python -m http.server 8000
timeout /t 2 /nobreak > nul
echo ========================================
echo ✅ Servers started!
echo 📊 Dashboard: http://localhost:8000/tnt_media_v3/dashboard.html
echo 🔌 API: http://localhost:8001
echo ========================================
start http://localhost:8000/tnt_media_v3/dashboard.html
pause
