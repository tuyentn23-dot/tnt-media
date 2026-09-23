# CLOUD DEPLOY - THONG TIN SAN SANG

## GitHub repo
- URL: https://github.com/tuyentn23-dot/tnt-media
- Private, branch main
- Commit: 7b3f630
- 1065 files, 0 secrets

## ClawCloud config
- Sign up bang GitHub (tuyentn23-dot)
- App Launchpad -> Create App
- Repository: tuyentn23-dot/tnt-media
- Branch: main
- Builder: Dockerfile
- Dockerfile path: deploy/Dockerfile
- Port: 8787
- RAM: 4GB, CPU: 2
- Env: GROQ_API_KEY=<copy tu .env>

## Sau khi deploy
1. Upload secrets qua File Browser:
 - memory/token_new_channel.json
 - config/token.pickle
 - memory/tnt_media.db
 - system/state.db
2. UptimeRobot ping /api/quotas moi 5 phut
3. Kiem tra https://<app>/api/quotas
