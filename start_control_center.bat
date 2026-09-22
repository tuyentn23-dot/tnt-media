@echo off
chcp 65001 >nul
title TNT Media Control Center
cd /d "%~dp0"
echo Dang khoi dong TNT Media Control Center...
python ops/control_center.py
pause
