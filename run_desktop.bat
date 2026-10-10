@echo off
REM Khoi dong TNT Media Studio (pythonw - no console)
setlocal
set VENV=%~dp0.venv\Scripts
set IMAGEIO_FFMPEG_EXE=%~dp0tools\ffmpeg.exe
cd /d %~dp0
start "" %VENV%\pythonw.exe "%~dp0desktop_app\app.py"
exit /b 0
