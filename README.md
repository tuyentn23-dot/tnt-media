---
title: TNT Media OS
emoji: 🎬
colorFrom: purple
colorTo: pink
sdk: docker
app_port: 7860
pinned: false
---

# TNT Media OS

Multi-channel YouTube Shorts automation for TNT Media.

## Services
- Scheduler (ops/scheduler_cc.py): publish theo cron moi kenh
- Dashboard (_serve.py): http://localhost:7860
- API: /api/quotas, /api/os/state, /api/status

## Env vars
- GROQ_API_KEY: bat buoc (content generation)

## Volume can upload
- memory/token_new_channel.json
- config/token.pickle
- memory/tnt_media.db
- system/state.db
