# YC5 - Deploy CLOUD khong can the tin dung

## CANH BAO QUAN TRONG
- Build video can ~1GB RAM moi tien trinh Python -> Koyeb free (512MB) se OOM khi build.
- Render free (512MB) cung OOM.
- => Chon nen tang >= 4GB RAM: ClawCloud Run hoac Zeabur (ca hai deu KHONG can the).

=========================================================
## PHUONG AN A - ClawCloud Run (khuyen nghi)
=========================================================
Mien phi: ~4 nhan 8GB container / thang (qua $5 credit). KHONG can the, chi can GitHub.

Buoc 1: Tao tai khoan
[ ] Mo https://run.claw.cloud/ -> Sign up bang GitHub

Buoc 2: Day code len GitHub
[ ] Tao repo private: tnt-media
[ ] cd D:/TNT_AI/venture_foundry/media
[ ] git init && git add . && git commit -m "TNT Media OS"
[ ] git remote add origin https://github.com/<user>/tnt-media.git
[ ] git push -u origin main

Buoc 3: Tao App tren ClawCloud
[ ] App Launchpad -> Create App -> GitHub repo tnt-media
[ ] Build: Dockerfile (deploy/Dockerfile)
[ ] Dockerfile path: deploy/Dockerfile
[ ] Port: 8787
[ ] RAM: 4GB, CPU: 2
[ ] Env vars: GROQ_API_KEY=...
[ ] Deploy

Buoc 4: Nap file bi mat (tokens + DB)
[ ] Dung File Browser cua ClawCloud hoac exec vao container:
[ ] memory/token_new_channel.json
[ ] config/token.pickle
[ ] memory/tnt_media.db
[ ] system/state.db

Buoc 5: Kiem tra
[ ] https://<app>.clawcloud.run/api/quotas
[ ] https://<app>.clawcloud.run -> dashboard

=========================================================
## PHUONG AN B - Zeabur
=========================================================
Mien phi: $5/thang, khong ngu neu du quota. KHONG can the.
[ ] Mo https://zeabur.com/ -> Sign up GitHub
[ ] New Project -> Deploy from GitHub -> chon tnt-media
[ ] Zeabur tu doc Dockerfile
[ ] Set port 8787, env GROQ_API_KEY
[ ] Upload tokens qua File tab

=========================================================
## PHUONG AN C - Koyeb (CHI de test, se OOM khi build)
=========================================================
Mien phi 512MB. Chi dung khi muon test dashboard/API, KHONG build video.
[ ] https://app.koyeb.com/ -> GitHub -> tnt-media
[ ] Builder: Dockerfile, path deploy/Dockerfile
[ ] Instance: Free (512MB), Port 8787

=========================================================
## GIU APP THUC (chong ngu)
=========================================================
[ ] Dang ky https://uptimerobot.com/ (mien phi, khong can the)
[ ] Add New Monitor -> HTTP(s)
[ ] URL: https://<app-url>/api/quotas
[ ] Interval: 5 phut
-> App luon thuc, khong bi ngu.

=========================================================
## LICH CHAY TU DONG
=========================================================
Container tu chay scheduler_cc.py (xem deploy/start.sh):
- Mialinhcute: 9h, 15h, 21h (gio UTC cua server)
- vilevi5676: 8h, 12h, 18h, 21h
Neu lech mui gio -> doi scheduleCron trong bang channels.

=========================================================
## CHECKLIST NHANH
=========================================================
1. [ ] Push code len GitHub
2. [ ] ClawCloud/Zeabur -> deploy tu GitHub
3. [ ] Set GROQ_API_KEY
4. [ ] Upload tokens + DB
5. [ ] UptimeRobot ping giu thuc
6. [ ] Mo /api/quotas kiem tra
7. [ ] Doi 9h/15h/21h xem clip moi len YouTube
