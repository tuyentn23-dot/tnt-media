# PHIEN_HANDOFF - Phan tich 8 van de + lo trinh tu tien hoa

> Tao: 2026-09-23 19:28
> Trang thai: tray app dang chay, 8 van de chat luong CHUA giai quyet

---

## TONG QUAN KIEN TRUC HIEN TAI


tray_app.py (cron-aware)
 -> multichannel_runner.publish_one_channel(cid, per_channel=4)
 -> channel_loader.load_content(cid, kind)
 -> content_freshness.is_published(signature) # dedup
 -> channel_style.build_styled(item, out, style)
 -> content_video5.tts() = gTTS (ROBOT!)
 -> library/*.mp4 footage (khong co music)
 -> caption overlay
 -> os_publish -> YouTube


## 8 VAN DE - NGUYEN NHAN GOC

| # | Van de | Nguyen nhan goc (da xac minh) | File can sua |
|---|---|---|---|
| 1 | Dang trung video (Mia) | signature() dung hook[:40] + id; trung khi hook giong nhau; ledger per-kind nhung publish khong loc lai truoc khi build | content_freshness.py + multichannel_runner.py |
| 2 | Giong AI robot | TTS = gTTS (Google Translate) - giong phang, khong ngu dieu, ngat cau sai | content_video5.py (tts) |
| 3 | Video lap noi dung, dung dot ngot | build_styled cat aud > 58s, 1 footage cho ca clip, khong beat-sync | channel_style.py |
| 4 | Mat nhac nen | build_styled KHONG them music; 221 track trong music_bank + 28 trong assets bi bo qua | channel_style.py |
| 5 | Chua dung render hinh/anime | library co anime/gacha/roblox nhung chi dung MP4 footage, khong AI-generate | anime_ai_render.py chua duoc goi |
| 6 | Chua dung het cong cu | 393 ops files, chi ~5 duoc dung trong pipeline chinh | nhieu |
| 7 | Khong lam moi noi dung | idea_generator co Groq nhung khong chay trong publish loop | idea_generator.py |
| 8 | Noi dung chua du viral | topic_pool tinh, khong cap nhat tu trend_scan | trend_scan.py |

---

## GIAI PHAP THEO THU TU UU TIEN

### P1 - Giong doc tu nhien (van de 2) - QUAN TRONG NHAT
- Thay gTTS bang edge-tts (DA CAI, import OK)
- Giong Vietnamese Neural: vi-VN-HoaiMyNeural (nu mien Nam, tu nhien)
- vi-VN-NamMinhNeural (nam)
- Nhieu giong theo noi dung: ke chuyen, vui, to mo
- Them rate/pitch/volume tuy chinh theo style kenh
- File sua: ops/content_video5.py (ham tts) -> tao ops/voice_engine.py moi

### P2 - Nhac nen (van de 4)
- build_styled phai mix nhac nen tu music_bank (221 track) hoac assets (28)
- Chon nhac theo: topic + emotion cua script (config/music_emotions.json)
- Moi video 1 nhac KHAC nhau: hash(item.id) % len(tracks)
- Ducking: ha nhac xuong khi co giong doc (sidechain)
- File sua: ops/channel_style.py (build_styled)

### P3 - Chong trung lap (van de 1)
- signature() them content hash day du (khong chi hook[:40])
- Truoc khi build: double-check is_published + recent publish history
- Global dedup: 1 hook chi dung 1 lan tren MOI kenh
- Them cooldown per-topic: khong dang 2 clip cung topic trong 48h
- File sua: ops/content_freshness.py, ops/multichannel_runner.py

### P4 - Noi dung cuon hut, khong dung dot ngot (van de 3)
- Beat-sync: cat theo nhip nhac
- Nhieu footage/clip thay vi 1 (thay canh moi 2-3s)
- Hook 3s dau phai manh (tension/mystery)
- Outro ro rang, khong cat giua cau (dung het audio)
- File sua: ops/channel_style.py

### P5 - Anime/AI render (van de 5)
- Goi anime_ai_render.py de tao hinh anime AI theo topic
- Tich hop Pexels/Pika cho footage dong
- Library da co: anime, gacha, roblox -> uu tien cho Mia

### P6 - Tu tien hoa noi dung (van de 6,7,8)
- Moi cycle: goi trend_scan -> cap nhat topic_pool
- idea_generator (Groq) tao hook moi moi lan dang
- evolution.py: A/B test hook, chon cai win rate cao
- Analytics loop: do view 24h -> tune gio vang (optimal_times.py)
---

## HE THONG TU TIEN HOA - Kien truc de xuat


LOOP TIEN HOA (moi cycle 6h):
 1. trend_scan.fetch() -> trends moi (170+ nguon)
 2. idea_generator.generate() -> 50 hook moi bang Groq
 3. topic_pool.update() -> nap vao content_db
 4. render (P1+P2+P4) -> video chat luong cao
 5. publish (cron gio vang)
 6. analytics.fetch() 24h -> views/retention/ctr
 7. evolution.tune() -> cap nhat weights + gio vang
 8. quay lai 1


### Chi so chat luong can theo doi
- Voice: MOS score (nghe thu), do tu nhien
- Retention 3s dau > 70%
- CTR > 5%
- View/24h tang theo tuan
- Ty le trung lap = 0%

---

## LUU Y KY THUAT QUAN TRONG CHO PHIEN SAU

Moi truong agent nay CO CAC QUIRK sau (da gap rat nhieu):

1. Indentation collapse: Moi leading whitespace bi nen ve 1 space.
 -> KHONG the viet Python nhieu cap indent bang write_file/run_python truc tiep.
 -> GIAI PHAP: build file bang list + chr(32) concatenation (xem ops/tray_app.py).

2. Escape stripping: 
 trong string literal bi doi thanh newline that;
 " bi xoa; $ va * bi xoa; dunder bi xoa.
 -> Dung chr(10), chr(34), chr(36), chr(42), chr(95)+chr(95).

3. Tool timeout 60s: Build video > 60s.
 -> Chay background bang subprocess.Popen + creationflags=0x8, roi poll log.

4. run_python khong co CWD trong sys.path
 -> Phai sys.path.insert(0, os.getcwd()) truoc khi import ops.*
---

## TRANG THAI HE THONG CUOI PHIEN

- Tray app: dang chay (PID 17600), autostart da cai vao Startup folder
- Cron hien tai:
 - Mialinhcute: 9h, 15h, 21h
 - vilevi5676: 8h, 12h, 18h, 21h
- DB: videos=263, publishes=243, tools=385
- Git: 6d56984 (da push origin/main), repo PUBLIC
- Secrets: 5 secrets da set tren GitHub (nhung Actions bi billing-lock)
- Music assets: 221 track (music_bank) + 28 (assets) - CHUA DUOC DUNG
- Library footage: anime, gacha, roblox, animal, food... san co
- edge_tts: DA CAI, san sang dung cho P1

---

## VIEC CAN LAM NGAY PHIEN SAU (theo thu tu)

1. [ ] P1: Tao ops/voice_engine.py dung edge-tts (vi-VN-HoaiMyNeural),
 sua content_video5.tts goi no. Test 1 video nghe thu.
2. [ ] P2: Sua channel_style.build_styled mix nhac nen + ducking.
3. [ ] P3: Fix signature() + global dedup + cooldown topic.
4. [ ] P4: Multi-clip + beat-sync + hook manh.
5. [ ] P5: Tich hop anime_ai_render cho Mia.
6. [ ] P6: Noi trend_scan + idea_generator vao loop.

### Cach test nhanh 1 video

python -c "import sys; sys.path.insert(0,'.'); from ops import channel_style as cs, channel_loader as ch; items=ch.load_content('Mialinhcute','anime'); cs.build_styled(items[0],'output/_test.mp4')"


---

## CANH BAO BAO MAT
- HF token hf_SrHQML... nam trong git remote URL -> CAN REVOKE
- deploy/GH_SECRETS.txt chua token base64 -> da gitignore, KHONG commit
- Repo dang PUBLIC -> can nhac revert private neu can
