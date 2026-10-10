# ============================================================
# QUY UOC BAT BUOC - DOC TRUOC KHI LAM BAT CU DIEU GI
# ============================================================
#
# Khi nguoi dung / bat ky ai trong du an nay noi "APP" / "ung dung" / "giao dien" / "UI" -> LUON LUON co nghia la:
#
# TNT Media Studio
# Shortcut: C:/Users/DELL/Desktop/TNT Media Studio.lnk
# Target: D:/TNT_AI/venture_foundry/media/run_desktop.bat
# Code: desktop_app/ (PyQt desktop app)
#
# KHONG PHAI web UI (app/ui/index.html + FastAPI :7777).
# Web UI chi la backend/dev tool, KHONG phai "app" nguoi dung dung.
#
# Sua chuc nang "app" -> sua trong desktop_app/.
# Sua API/backend -> sua trong app/server.py + pipeline/.
#
# ============================================================

# QUY TAC CHAT LUONG (KHONG DOI)
Moi video PHAI:
- Dai 15-30 giay
- Noi dung LQ den query (Pexels match)
- Khong lap video da dang trong 30 ngay
- Fade out cuoi
- Giong doc >= 80 ky tu
Vi pham -> quality_gate chan, KHONG dang.
Xem quality_policy.json

# AGENT_RULES - Quy tac bat buoc cho AI agent

## BUOC 0 - BAT BUOC DAU TIEN

DOC FILE BOOTSTRAP.md TRUOC KHI LAM BAT CU DIEU GI.

Sau do chay:


python -m guardian.agent_boot


Lenh nay in ra:
- Kien truc he thong (pipeline/modules/app/state/guardian)
- Trang thai DB + git
- Danh sach critical file CAM SUA
- Modules hien co (agent lam viec o day)
- Tai lieu phai doc

## TRUOC KHI LAM

1. Doc BOOTSTRAP.md (file goc)
2. Doc STATE.md + CHANGELOG.md + PIPELINE_SPEC.md
3. Chay: python guardian/guard.py before (snapshot)

## TRONG KHI LAM

- KHONG dung os.remove / Remove-Item / rm truc tiep
- Xoa file: python guardian/safe_fs.py remove <file>
- Khong xoa hang loat (glob + remove)
- Dung absolute path hoac cd dung workspace
- Kiem tra git status truoc khi thao tac file
- KHONG SUA: pipeline/, state/pipeline.db, guardian/, app/server.py
- CHI SUA: modules/, ops/ (neu can thiet)

## SAU KHI LAM XONG

1. Chay: python guardian/guard.py verify
2. Chay: python -m pipeline.selfcheck
3. Chay: python -m pytest tests/ -q

Ca 3 PHAI PASS.

## 4 YEU CAU 100% BAT BUOC

1. NHO MOI LAN - chay agent_boot dau phien, cap nhat CHANGELOG.md cuoi phien
2. KHONG SAI - chay tests/ truoc commit, selfcheck sau khi sua
3. KHONG PHA CAI DA LAM - khong sua pipeline/, state/pipeline.db, guardian/
4. 100% DAM BAO - checklist trong BOOTSTRAP.md muc 8 phai dat het


## VIDEO ENGINE CONTRACT (2026-10-08)

TNT Media ho tro nhieu engine tao video (mien phi + cloud API).
Moi video sinh ra qua app PHAI co day du metadata sau:

### Engine co san
| Engine | Provider | Free | API | Trang thai |
|---|---|---|---|---|
| pexels | Pexels.com | YES | REST | DA TEST OK (1080x1920, audio day du) |
| luma | LumaLabs | YES (can key) | REST | Key hien co khong dung loai |
| fal | fal.ai | YES (can key) | fal_client | Chua co key |
| replicate | Replicate | YES (can key) | REST | Chua co key |
| kling | KlingAI | YES (can key) | REST | Chua co key |
| wavespeed | WaveSpeed | YES (can key) | REST | Chua co key |
| flow | Google Flow/Veo | YES | CDP (Playwright) | DA TEST OK v7.0.0 (720p, 10s, audio) |
| vids | Google Vids | YES | Playwright | Chua test |
| gacha | Local code | YES | Python | DA TEST OK |
| ffmpeg | Local binary | YES | subprocess | DA TEST OK |

### API Endpoints
- GET /api/video/engines -> danh sach engine + trang thai
- POST /api/video/generate -> tao video tu prompt (body: prompt, engine, duration, channel)
- GET /api/video/engine/{name}/health -> test 1 engine

### Signature bat buoc
- Response co field tnt_engine (provider, model, is_free, elapsed_sec, generated_by)
- Log co dong [TNT-MEDIA-ENGINE] provider=... model=... free=true elapsed=...s

### UI
- Tab "Video Engines" trong app: bang engine + form generate + ket qua

### Quy tac
- KHONG goi truc tiep modules.video.* tu ngoai pipeline -- phai qua dispatcher modules/render/video.py
- Engine moi: them vao ENGINE dict trong modules/render/video.py
- Fallback order: flow -> vids -> luma -> pexels -> ffmpeg


## VOICE + PRESET CONTRACT (2026-10-09)

TNT Media ho tro 6 giong doc + 8 sac thai (preset), tat ca mien phi qua edge-tts.

### Giong doc (VI_VOICES) - modules/voice/edge_tts.py
| id | Giong | Ghi chu |
|---|---|---|
| female_north | HoaiMy | vi-VN, nu Bac, MAC DINH |
| male_north | NamMinh | vi-VN, nam Bac |
| female_multilingual | Ava | da ngon ngu |
| female_emma | Emma | da ngon ngu |
| female_jenny | Jenny | da ngon ngu |
| male_andrew | Andrew | da ngon ngu |

### Sac thai (PRESETS) - rate / pitch / volume
| id | Y nghia | rate | pitch | volume |
|---|---|---|---|---|
| default | Mac dinh | +0% | +0Hz | +0% |
| cheerful | Vui ve (mac dinh pipeline) | +15% | +30Hz | +5% |
| sad | Buon | -15% | -20Hz | +0% |
| excited | Hao hung | +25% | +40Hz | +8% |
| calm | Diem tinh | -10% | -10Hz | -5% |
| narrator | Ke chuyen | -5% | +0Hz | +0% |
| kids | Tre em | +10% | +50Hz | +5% |
| news | Tin tuc | +8% | -5Hz | +3% |

### API
- GET /api/config/voices -> 6 giong {id, label, voice}
- GET /api/config/presets -> 8 preset {id, label, rate, pitch, volume}

### Luong override (job -> render)
1. UI gui voice_override + voice_preset trong POST /api/jobs
2. runner merge vao style: style[voice], style[voice_preset], style[preset]
3. modules/render/voice_synth.synth_words(voice, preset) ap dung
4. Cot jobs.voice_preset luu trong state/pipeline.db

### STOCK FALLBACK CONTRACT (2026-10-09)

Khi Pexels khong du clip, tu dong fallback sang Pixabay + Coverr.
- Module: modules/render/stock_fallback.py
- Tich hop: modules/render/pexels_builder.build() goi fallback khi < 2 clip
- API keys (tuy chon, mien phi): PIXABAY_API_KEY, COVERR_API_KEY trong .env
- Khong co key -> tra [] (graceful, khong crash)
- Thu tu: Pexels -> Pixabay -> Coverr

