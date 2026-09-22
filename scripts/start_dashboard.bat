@echo off
echo ============================================
echo   TNT Media Dashboard
echo ============================================
echo.
cd /d "%~dp0.."
echo Starting dashboard at http://localhost:8000
echo Press Ctrl+C to stop
echo.
python scripts\start_dashboard.py
pause
