# CHANGELOG - XEM _archive_CHANGELOG.md cho lich su cu

## 2026-09-22 (phien Noi A->B + YC2/3/4/7 + Fix publish)
- Noi Nhanh A (memory/tnt_media.db) vao Nhanh B (system/state.db): ops/sync_a_to_b.py, tich hop vao state_sync.py
- YC3: viet lai ops/trend_scan.py (Google Suggest free) -> 170 trends
- YC4: viet lai ops/decision_engine.py (trends -> decisions, idempotent)
- YC2: ops/idea_generator.py (Groq openai/gpt-oss-120b) -> 6 y tuong moi
- YC7: them GET /os/api/state doc Nhanh B vao dashboard
- YC1: ops/decision_to_publish.py (dry-run mac dinh)
- FIX BUG moviepy: shim with_* -> set_* trong ops/compat.py (venv la moviepy 1.0.3)
- FIX script MIA: them 5 topic co dau tieng Viet vao config/scripts_vi.json
- FIX nhac: _music_for chon tu music_bank/ (221 bai) thay vi 6 bai library
- PUBLISH TEST: Mialinhcute 4 clip (anime lf5wVD-JXlU, roblox zVLfPtk3E5U, cute_animals o-7fNEJKNFE, meme VJv21IYSqvk)

## 2026-09-21 (phien Kids + ViLe Vi + Anime AI)
- 5 video ViLe Vi facts da dang (octopus/moon/shark/brain/heart)
- 5 video Mia kids da dang (gacha/roblox/anime/cat/pikachu)
- 8 video Mia teen da dang (pikachu/gacha/bully/cold/wheel/meme/drama/cool)
- Tools moi: gacha_anime_render, anime_ai_render, build_mia_kids, build_vile_short
- Content moi: mia_content_kids, vile_content, content_v2, gacha_viral_pack
- QG rieng cho ViLe Vi: quality_gate_vile
- Fix: font Segoe UI (khong Arial Black), caption drawtext dung relative path

Xem SESSION_HANDOFF.md de biet chi tiet day du.

## 2026-09-22 (phien YC1: noi decision B vao autopublish)
- ops/autopublish_runner.py: them _decision_topic() doc decision_to_publish.choose(3), dung footage lam topic build video; fallback topic_picker khi khong co decision
- Da compile OK; _decision_topic tra ve footage hop le

## 2026-09-22 (phien dang 4 clip moi - 2 kenh dung style)
- Mialinhcute: anime_sailormoon https://youtu.be/SS13ejNumtU | roblox_piggy https://youtu.be/0Bvwg9uh8ws (score 80)
- vilevi5676: v_market_morning https://youtu.be/xeieMfkPqFk | v_rain_saigon https://youtu.be/ohv0anIryiw (score 80)
- Dung ops/channel_producer.run_many(cid, limit=2, live=True): content_db.json rieng tung kenh + quality gate + token rieng
- state_sync A->B: videos=255 publishes=235 analytics=26

## 2026-09-22 (phien 4 - hoan tat 7 YC)
- YC1 XONG: ops/scheduler_cc.py (cron 5 truong, doc scheduleCron tung kenh, chay channel_producer.run_many)
- YC4 XONG: ops/weights_tuner.py (hoc tu memory/tnt_media.db metrics) + decision_engine dung weights
- YC5 XONG artifacts: deploy/oracle_setup.sh, tnt-scheduler.service, tnt-dashboard.service, README_ORACLE.md
- YC6 XONG: ops/evolution.py - 3 cap (A/B prompt, weight tuning, tool gen+approve)
- YC7 XONG: ops/os_api.py (quota per channel + /api/quotas + /api/os/state) moc vao control_center
- YC2/YC3 da XONG tu truoc
- Tat ca module compile OK; state_sync A->B: videos=255 publishes=235 tools=385

## 2026-09-23 (phien 5 - test 8 clip moi, 4/kenh dung rule)
- Mialinhcute: roblox_arsenal xiSXKm_KJTg | roblox_jailbreak YboaI7Rmfdc | animal_panda 3U8RdfVjLqM | animal_fennec RogmlM6mTgI (score 80)
- vilevi5676: v_why_dejavu MAzJCIPN5dw | v_why_hair_gray rw5tC9jX5_4 | moon_drift tykeuQ85qk4 | octopus3heart 2wFyx_7XuJM (score 80)
- Tao requirements.txt, deploy/push_to_vm.sh, deploy/CHECKLIST.md cho YC5
- YC5 cho tai khoan Oracle (cho credit card)
- state_sync A->B: videos=263 publishes=243

## 2026-09-23 (phien 6 - chuan bi deploy cloud khong the)
- Tao git repo RIENG trong media/ (tach khoi D:/TNT_AI), commit 1065 files, 0 secrets
- Chan secrets: token.pickle, config/client_secrets.json, .env, *.db
- cloud_media/ 313MB (36 clip + 10 nhac) cho cloud build
- Dockerfile + start.sh + docker-compose + requirements.txt
- deploy/prepare_cloud_media.py, git_push_cloud.sh, README_CLOUD.md
- Huong dan: ClawCloud (~8GB, khong the) / Zeabur / Koyeb(512MB->OOM)
- Buoc tiep: user push len GitHub -> deploy ClawCloud

## 2026-09-23 (phien 6 - chuan bi deploy cloud khong the)
- Tao git repo RIENG trong media/ (tach khoi D:/TNT_AI), commit 1065 files, 0 secrets
- Chan secrets: token.pickle, config/client_secrets.json, .env, *.db
- cloud_media/ 313MB (36 clip + 10 nhac) cho cloud build
- Dockerfile + start.sh + docker-compose + requirements.txt
- deploy/prepare_cloud_media.py, git_push_cloud.sh, README_CLOUD.md
- Huong dan: ClawCloud (~8GB, khong the) / Zeabur / Koyeb(512MB->OOM)
- Buoc tiep: user push len GitHub -> deploy ClawCloud
