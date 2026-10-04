@echo off
REM media.bat - Chay media/ voi venv rieng
REM Su dung: media.bat <script.py> [args]
setlocal
set VENV=%~dp0.venv\Scripts
set IMAGEIO_FFMPEG_EXE=%~dp0toolsfmpeg.exe
"%VENV%\python.exe" %*
