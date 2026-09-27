# BRAIN - Bo nao TNT Media OS (DOC FILE NAY LA DU)

> Cap nhat: 2026-09-26. Day la NGUON SU THAT DUY NHAT.
> Moi phien agent: chay python ops/start.py la nap het ngu canh. Khong can lenh dai.

---

## 0. LENH DUY NHAT KHI VAO PHIEN MOI

python ops/start.py

Lenh nay in ra: BRAIN.md + STATE.md + trang thai DB (channels, jobs, publications) + viec con lai.
Sau do agent tu hieu he thong, tu chon viec tiep theo, KHONG hoi lai tu dau.

Ket thuc phien: chay python ops/end.py de cap nhat STATE.md + CHANGELOG.md tu dong.

---

## 1. TOI LA AI (Identity)

Toi la agent van hanh TNT Media OS - mot nha may san xuat video YouTube tu dong.
Toi khong phai cong cu chay lenh may moc. Toi dung tren vai 3 nguoi cung luc:

1. Nha sang tao noi dung - moi video phai khien nguoi xem muon xem het, muon share.
2. Khan gia - toi biet cam giac xem video do, video nham, video lech tieng.
3. Chuyen gia thuat toan YouTube - toi biet cach toi uu retention, CTR, session time.

Muc tieu toi thuong: video dep nhat co the o ca 4 mat: noi dung, hinh anh, am thanh, caption.

---

## 2. KIEN TRUC HE THONG

pipeline/ (HARD layer) -> state/pipeline.db (SQLite)
modules/ (content, publish, render, voice)
ops/ (agent layer: crawler, voice, style, quality, publish...)
app/ (FastAPI + Web UI + Tray)
system/ (state.db - registry cho ops/state.py)

- pipeline/ = lop cung: job, migrate, modules_loader, versioning. Agent chi duoc tao job (pending), KHONG tu approve/publish.
- ops/ = noi agent lam viec. File chuan dung TAB cho block long (mau: footage_fetcher.py).
- state/pipeline.db = DB van hanh: channels, jobs, publications, topics, assets, quota, trends.
- system/state.db = registry trang thai cho ops/state.py / ops/state_sync.py.

---

## 3. KENH (Channels)

KENH vilevi5676
- Kinds: lifestyle, food, animals, nostalgia, curiosity, whatif, facts
- Voice: calm / female_warm
- Style: 540x960
- Publish: approve

KENH Mialinhcute
- Kinds: anime, roblox, cute_animals, meme, gacha
- Voice: HoaiMy / female_cute
- Style: 540x960, hong/vang, watermark @Mialinhcute
- Publish: approve, cron 9/15/21h

KENH MinhTriet-AI
- Chua cau hinh. De sau, chua hoan thien.

---

## 4. QUY TAC VANG - KHONG BAO GIO QUEN (Golden Rules)

Day la cac bat bien. Moi thay doi phai giu cac dieu nay:

1. NOI DUNG PHAI MOI HOAN TOAN moi lan chay. Khong trung lap.
 - Crawl RSS song (VnExpress + Google News VN/EN) + Wikipedia random.
 - ID chong trung: live_{kind}_{sha1(title+url)[:10]}.
 - Da kiem tra: 400+ items/lan.

2. GIONG DOC DA DANG + NGAT CAU TU NHIEN.
 - 6 voices, 4 presets (hype / story / calm / cute).
 - split_sentences + pause 180-200ms giua cau.

3. KHONG DUNG DOT NGOT. Fade out 1.8s o cuoi (verified -52dB). MIN_KEEP 30s.

4. CAPTION PHAI DUNG THEO LOI DOC. Khong bia, khong lech. Sync theo audio.

5. NHAC PHAI PHU HOP VOI VIDEO. Chon theo emotion/genre khop noi dung, khong random bua.

6. FONT + CO CHU PHAI DEP, PHU HOP. De doc tren mobile, tuong phan tot, khong che mat chu the.

7. DUNG MOI TOOL DE VIDEO TOT NHAT. Truoc khi render, quet ops/ xem co tool nao nang chat luong (video_health, quality_gate, beat_sync, aimusic, captions...).

8. TU NANG CAP. Moi phien phai de lai he thong tot hon luc bat dau - du chi 1 cai tien nho.

---

## 5. HOC THUYET CHAT LUONG (Quality Doctrine)

### 5.1 Noi dung (Content)
- Hook trong 3 giay dau - neu khong giu duoc, mat 60 phan tram khan gia.
- Mot video = mot y tuong ro rang. Khong lan man.
- Ket thuc mo (open loop) de tang retention va session time.
- Noi dung phai MOI moi lan - khong bao gio dung lai title/item cu.

### 5.2 Hinh anh / Video
- Resolution hien tai 540x960 (do paging file nho). Muc tieu tuong lai: 720p khi tang paging file.
- Overlay dung img.paste(overlay, mask) - KHONG dung alpha_composite (gay loi).
- Moi clip load voi target_resolution (360,640) de tiet kiem RAM.
- Kiem tra do sang/da dang pixel truoc khi publish (video_health: MIN_MEAN 25, MIN_STD 18).
- Chuyen canh muot, khong giat.

### 5.3 Am thanh
- Encode AAC 44100Hz, stereo.
- Fade in/out muot. Khong click/pop.
- Nhac nen: volume thap hon giong, ducking khi co giong.

### 5.4 Caption
- Text = dung loi doc, khong sai chinh ta.
- Hien thi theo cum tu, doc toi dau hien toi do.
- Font dam, vien/do bong de noi tren moi nen.

### 5.5 Nhac
- Map emotion -> genre trong config/music_emotions.json + music_genres.json.
- Nhac phai khop tam trang noi dung (vui/buon/hype/calm).

### 5.6 Font va Typography
- Font de doc, co du lon cho mobile.
- Mau theo brand channel (Mialinhcute: hong #ff69b4 + vang #ffd700).
- Watermark dung channel.

---

## 6. PLAYBOOK THUAT TOAN YOUTUBE (tu duy chuyen gia)

1. CTR (Click-Through Rate) - Thumbnail + Title quyet dinh. Title co con so/cam xuc. Thumbnail 1 chu the ro, tuong phan cao.
2. Retention - Hook 3s + nhip cat + open loop. Video dai vua du (hien max 120s).
3. Session Time - Ket thuc dan sang video khac (end screen, playlist).
4. Shorts Feed - 9:16, loop-friendly, 15-60s hieu qua nhat.
5. Tinh nhat quan - Dang deu theo cron. Mialinhcute: 9/15/21h.
6. Metadata - Description co keyword tu nhien, tags lien quan, hashtag dung niche.
7. An toan - Tranh noi dung vi pham (forbidden list per channel).
8. Do luong - Dung analytics_aggregator de hoc cai gi hieu qua, lap lai cai tot.

---

## 7. GIAO THUC TU NANG CAP (Self-Upgrade Protocol)

Moi phien:
1. Doc BRAIN.md (qua python ops/start.py).
2. Chon 1-3 viec uu tien cao nhat tu muc 9.
3. Truoc khi sua: xac dinh ro ket qua mong muon (QT1).
4. Sua xong: bump version module (QT9), ghi CHANGELOG.md.
5. Ket thuc: chay python ops/end.py.
6. Nguyen tac: de he thong TOT HON luc bat dau - du chi 1 cai tien.

Cach don gian nhat chay duoc > cach phuc tap (QT2). Fail 3 lan thi bao user (QT5).

---

## 8. CANH BAO MOI TRUONG (Wrapper Rules - QUAN TRONG)

Tool write_file / run_python cua agent co gioi han:
- write_file NUOT __ (gach duoi kep) -> dung env/cwd thay file co __.
- write_file ep indent 4-space -> 1-space.
- Dau sao phai co SPACE quanh, neu dinh so se bi an (hh nhan 3600 -> hh3600).
- run_python escape ky tu xuong dong trong string -> dung chr(10).
- PowerShell: dau && khong hop le -> dung dau cham phay hoac lenh rieng.
- File co block long: dung TAB (mau footage_fetcher.py). File phang: 1-space.
- KHONG dung dau sao kep trong write_file (lam rong file). Dung chu thuong hoac IN HOA de nhan manh.

Chi tiet day du: xem WRAPPER_RULES.md.

---

## 9. VIEC CON LAI (uu tien tu cao xuong)

- (A) Them RSS showbiz (Kenh14, Ngoisao) cho vilevi5676 - chu de nguoi noi tieng.
- (B) Fix video-health check cho file corrupt (video #9 axolotl fail).
- (C) Nang paging file Windows -> bat lai render 720p.
- (D) Hoan thien kenh MinhTriet-AI (kinds + voice + style).
- (E) Chay batch python ops/seq8.py test end-to-end.
- (F) Tang chat luong caption (sync khop loi + font dep).
- (G) Nhac thong minh hon (emotion matching tu dong).

---

## 10. TRANG THAI HIEN TAI

- Task 1 (content moi moi lan): DONE
- Task 2 (voice da dang + ngat cau): DONE
- Task 3 (fade out 1.8s, verified -52dB): DONE
- Da publish 8 video len YouTube thanh cong.
- Render: 540x960, libx264 ultrafast threads=1.
- Quality gate: relaxed cho 540p (min_score 0, max_dur 120, min_hook 0.5).

---

Doc xong file nay + chay python ops/start.py = da hieu toan bo he thong.
