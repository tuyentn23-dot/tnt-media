# TNT MEDIA v2 - HANDOFF PROTOCOL

## Quy trinh handoff giua cac phien

---

## KHI BAT DAU PHIEN MOI

### 1. Doc cac file theo thu tu:
1. `tnt_media_v2/docs/CHECKPOINT.md` - Trang thai hien tai
2. `tnt_media_v2/docs/ROADMAP.md` - Lo trinh chi tiet
3. `TNT_MEDIA_MASTER_PLAN.md` (thu muc goc) - Chien luoc tong the

### 2. Xac dinh cong viec tiep theo
- Chon task tu CHECKPOINT.md phan 'CHUA HOAN THANH'
- Uu tien theo thu tu da danh so

### 3. Kiem tra moi truong
- Python libraries da cai
- API keys da co
- File video/audio da tao

---

## TRONG KHI LAM VIEC

### Ghi nhat ky moi buoc:
- Tao file `tnt_media_v2/docs/SESSION_LOG.md`
- Ghi ro: da lam gi, ket qua, loi gap phai

### Luu tru code:
- Tat ca code moi vao `tnt_media_v2/generators/` hoac `tnt_media_v2/pipeline/`
- Khong sua code cu neu khong can

### Test truoc khi chuyen tiep:
- Chay thu module moi
- Kiem tra output
- Ghi lai ket qua

---

## KHI KET THUC PHIEN

### Cap nhat CHECKPOINT.md:
- Danh dau cac muc da hoan thanh
- Them cac muc chua hoan thanh moi

### Cap nhat SESSION_LOG.md:
- Tom tat cong viec da lam
- Ghi loi gap phai va cach giai quyet
- Ghi y tuong cho phien sau

### Luu tat ca file:
- Code moi vao thu muc dung
- Du lieu vao output/
- Config vao config/

---

## CAU TRUC THU MUC CHUAN

```
venture_foundry/media/
├── TNT_MEDIA_MASTER_PLAN.md
├── tnt_media_v2/
│   ├── README.md
│   ├── docs/
│   │   ├── ROADMAP.md
│   │   ├── CHECKPOINT.md
│   │   ├── HANDOFF_PROTOCOL.md
│   │   └── SESSION_LOG.md
│   ├── agents/
│   │   └── (research, script, seo)
│   ├── generators/
│   │   ├── visualizer_engine.py
│   │   ├── thumbnail_generator.py
│   │   └── (voice, image, music)
│   ├── pipeline/
│   │   ├── orchestrator.py
│   │   ├── auto_publisher.py
│   │   └── (quality_checker, scheduler)
│   ├── config/
│   │   └── channels_config.json
│   └── output/
│       ├── videos/
│       └── thumbnails/
├── output/
│   ├── visualizer_FINAL.mp4
│   └── spectrum_data.npy
├── library/
│   └── (audio files)
├── memory/
│   └── published_videos.json
├── token.pickle
└── client_secret_*.json
```

---

## CAC API CAN TAO

| API | URL | Free tier | Ghi chu |
|-----|-----|-----------|---------|
| Suno AI | suno.com | 10 bai/ngay | Tao nhac |
| ElevenLabs | elevenlabs.io | 10k ky tu/thang | Giong noi |
| HuggingFace | huggingface.co | Unlimited | Models AI |
| Replicate | replicate.com | Co credit free | API AI |

---

## QUY UOC DAT TEN

- Modules: `ten_module.py` (snake_case)
- Classes: `TenClass` (PascalCase)
- Functions: `ten_ham()` (snake_case)
- Config: `ten_config.json`
- Output: `ten_output.mp4`

---

## LENH THUONG DUNG

```bash
# Chay orchestrator
cd tnt_media_v2 && python pipeline/orchestrator.py

# Kiem tra cac module
python -c "from generators.visualizer_engine import AudioVisualizerEngine"

# Xem trang thai
cat tnt_media_v2/docs/CHECKPOINT.md
```
