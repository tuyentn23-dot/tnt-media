@echo off
cd /d "D:\TNT\AI\venture\foundry\media"
set PYTHONPATH=%CD%
set DASH_PORT=8787
"D:\TNT\AI\venv\Scripts\python.exe" ops\control_center.py
