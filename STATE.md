# STATE - TNT MEDIA
Cap nhat: 2026-09-21 17:15

## KENH (2)
- Mialinhcute (Mia Linh Cute): 9:16, max 20s, voice female_cute
 Niche: kids (8-10t) + gacha/anime. KHONG romance.
 QG: quality_gate | Content: channels/Mialinhcute/
- vilevi5676 (ViLe Vi): 9:16, max 90s, voice female_warm
 Niche: facts/khoa hoc/lifestyle
 QG: quality_gate_vile | Content: channels/vilevi5676/

## TOOLS CHINH (trong ops/)
- Publish: os_publish.py (OP.set_channel -> OP.publish)
- Build: build_mia_kids.py, build_vile_short.py, gacha_anime_render.py
- Voice: voice_synth.py (edge-tts vi-VN-HoaiMy, mien phi)
- AI anh: Pollinations.ai (mien phi, ~50s/anh, model=flux)
- QG: quality_gate.py, quality_gate_vile.py
- Content: mia_content_kids.py, vile_content.py, content_v2.py

## DA DANG 2026-09-21
- ViLe Vi (5 facts): rZ9m-xNkfzQ, AD4TDjv0zCs, 58t6V0phaNA,
 KLtoIncoQbE, ylQa4T7Ouro
- Mia kids (5): wXTWNNzux40, Hl4tJn3kEL4, e-4Wve3xOco,
 q99YwEGm2Xg, 0vI0FhLtqGc (+1dKFfb670j4 TRUNG)
- Mia teen (8): 32wKURhZ1ac, RjMvJ0sMlDI, A1HcbvI2Q2s, 8aGPzyNHxfk,
 YqE5nu2Sp9g, mwpU1rktyZg, PXjImhkW_Bg, uVdkNMXVlOY

## TODO
Cao:
1. Xoa pikachu trung 1dKFfb670j4 (Studio thu cong)
2. Xoa video gacha crush cu (Studio thu cong)
3. Batch Mia kids: Minecraft, Among Us, Hello Kitty, Sonic
4. Batch ViLe Vi: ~20 item content_db con lai

Trung: caption word-by-word, duration 30-40s, img2img nhat quan

## CANH BAO QUAN TRONG
1. Token thieu youtube.force-ssl -> khong xoa video qua API (Studio thu cong)
2. Font tieng Viet: Segoe UI Bold (KHONG Arial Black - mat dau)
3. Wrapper strip __ va indent -> dung TAB + verify bang zz_verify.py
4. drawtext: relative path (khong D: vi : bi parse loi)
5. Kenh Mia: huong tre em, KHONG romance
6. Tra loi user: tieng Viet CO DAU
7. Build video dai: subprocess.Popen + DETACHED_PROCESS (tranh timeout 60s)

## QUY TRINH PUBLISH (7 quy tac)
a) OP.set_channel(cid) TRUOC khi publish
b) privacy=public (unlisted bi YouTube xoa)
c) topic UNIQUE: cid + timestamp
d) title = hook[:90] + #shorts
e) CHI dang video DA PASS quality_gate
f) desc = hook + 2 newline + hashtags
g) force=True de bypass check trung

## LENH MAU
Build 1 video (background):
 python -c "import subprocess,os,sys; p=subprocess.Popen(
 [sys.executable,'ops/build_mia_kids.py','gacha_school'],
 creationflags=0x00000008|0x00000200)"

Sinh anh AI:
 URL: https://image.pollinations.ai/prompt/{prompt}
 ?width=768&height=1024&model=flux&seed=101&enhance=true

## THAM KHAO THEM
- _archive/root_docs/ : file context cu (neu can dao sau)
- Code trong ops/ : nguon chan ly cho tools/rules
