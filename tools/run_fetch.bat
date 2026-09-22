@echo off
cd /d D:\TNT_AI\venture_foundry\media
python tools/fetch_mia_footage2.py 1> logsm3.out 2> logsm3.err
echo DONE >> logsm3.out
