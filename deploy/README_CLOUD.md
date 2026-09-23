# YC5 - Deploy CLOUD khong can the tin dung

## TRANG THAI HIEN TAI
- [x] Code da commit vao git repo rieng trong media/ (1065 files, khong co secrets)
- [x] cloud_media/ (313MB, 36 clip + 10 nhac) da san sang
- [x] Dockerfile + start.sh + compose
- [ ] Push len GitHub
- [ ] Deploy ClawCloud

=========================================================
## BUOC 1 - PUSH LEN GITHUB
=========================================================
1. Mo https://github.com/new
2. Repository name: tnt-media
3. Chon Private -> Create repository
4. Copy URL dang: https://github.com/<user>/tnt-media.git
5. Mo terminal (Git Bash / PowerShell) va chay:

 cd D:/TNT_AI/venture_foundry/media
 git remote add origin https://github.com/<user>/tnt-media.git
 git push -u origin main

(Neu hoi dang nhap: dung Personal Access Token thay password)

=========================================================
## BUOC 2 - DEPLOY CLAWCLOUD (khuyen nghi, ~8GB RAM)
=========================================================
1. Mo https://run.claw.cloud/ -> Sign up bang GitHub
2. App Launchpad -> Create App -> chon repo tnt-media
3. Build config:
 - Builder: Dockerfile
 - Dockerfile path: deploy/Dockerfile
 - Port: 8787
4. Resources: RAM 4GB, CPU 2
5. Environment variables:
 - GROQ_API_KEY = <key cua ban trong .env>
6. Deploy -> doi ~3-5 phut build

=========================================================
## BUOC 3 - UPLOAD SECRETS LEN CLOUD
=========================================================
Sau khi app chay, dung File Browser cua ClawCloud de upload:
- memory/token_new_channel.json (YouTube token Mia)
- config/token.pickle (YouTube token ViLe)
- memory/tnt_media.db (ledger A)
- system/state.db (state B)

=========================================================
## BUOC 4 - GIU APP THUC
=========================================================
1. Mo https://uptimerobot.com/ -> Sign up mien phi
2. Add New Monitor -> HTTP(s)
3. URL: https://<app-url>/api/quotas
4. Interval: 5 phut
-> App khong bi ngu.

=========================================================
## BUOC 5 - KIEM TRA
=========================================================
- https://<app-url>/ -> dashboard
- https://<app-url>/api/quotas -> quota 2 kenh
- Log: container logs tren ClawCloud

Lich chay tu dong (gio UTC server):
- Mialinhcute: 9h, 15h, 21h
- vilevi5676: 8h, 12h, 18h, 21h

=========================================================
## PHUONG AN DU PHONG
=========================================================
- Zeabur: https://zeabur.com/ (GitHub signup, $5/thang free)
- Koyeb: 512MB -> CHI test duoc dashboard, build video se OOM
- GitHub Actions: thay the toan bo (xem phuong an A trong phien truoc)
