# TNT MEDIA v2 - ROADMAP CHI TIET

## Muc tieu tong the
Xay dung he thong AI YouTube automation hang dau cho kenh @vilevi5676
Niche: Nhac tru tinh Viet Nam

---

## PHASE 1: AUDIO ENGINE (Uu tien cao nhat)

### 1.1 Tich hop Suno AI API (1 ngay)
- Dang ky tai suno.com
- Lay API key (free: 10 bai/ngay)
- Cai dat: pip install requests
- Tao module: agents/suno_client.py
- Test: Tao 1 bai nhac tru tinh tieng Viet

### 1.2 Tich hop Coqui TTS cho tieng Viet (1 ngay)
- Cai dat: pip install TTS
- Download model: xtts_v2 (ho tro tieng Viet)
- Tao module: generators/voice_generator.py
- Test: Doc 1 doan van tieng Viet

### 1.3 Audio Enhancement (0.5 ngay)
- Dung pydub de normalize
- Them reverb, EQ bang FFmpeg
- Tao module: pipeline/audio_enhancer.py

---

## PHASE 2: VISUAL ENGINE (Uu tien cao)

### 2.1 Cai dat Stable Diffusion (1-2 ngay)
- Cai dat AUTOMATIC1111 WebUI
- Tai model: DreamShaper v8 hoac Anything V5
- Tao API endpoint
- Module: generators/image_generator.py

### 2.2 AnimateDiff cho animation (1 ngay)
- Cai dat AnimateDiff extension
- Tao animation tu prompt
- Module: generators/animation_generator.py

### 2.3 Nang cap Visualizer (1 ngay)
- Them che do waveform
- Them circular spectrum
- Them particle effects
- Them color themes

---

## PHASE 3: CONTENT PIPELINE (Uu tien trung binh)

### 3.1 Research Agent (1 ngay)
- Dung YouTube Data API de phan tich kenh doi thu
- Tim keyword trending
- Module: agents/research_agent.py

### 3.2 SEO Optimizer (0.5 ngay)
- Tu dong tao title
- Tu dong tao description
- Tu dong tao tags
- Module: agents/seo_optimizer.py

### 3.3 Quality Checker (0.5 ngay)
- Kiem tra video quality
- Cham diem 1-10
- Module: pipeline/quality_checker.py

---

## PHASE 4: AUTOMATION (Uu tien trung binh)

### 4.1 Smart Scheduler (0.5 ngay)
- Dang video gio vang
- Lich dang tu dong
- Module: pipeline/scheduler.py

### 4.2 Analytics Dashboard (1 ngay)
- Theo doi views, retention
- Bao cao hang ngay
- Module: pipeline/analytics.py

### 4.3 A/B Testing (1 ngay)
- Test title/thumbnail
- Tu dong chon tot nhat
- Module: pipeline/ab_tester.py

---

## API CAN SU DUNG (chi phi thap)

| API | Chi phi | Muc dich | Uu tien |
|-----|---------|----------|---------|
| Suno AI | Free (10 bai/ngay) | Tao nhac | CAO |
| Coqui TTS | Free (open source) | Giong noi tieng Viet | CAO |
| Stable Diffusion | Free (local) | Hinh anh AI | CAO |
| YouTube Data API | Free (10,000 units/ngay) | Dang video, analytics | CAO |
| ElevenLabs | $5/thang (30 phut) | Giong noi chat luong cao | Trung binh |
| Midjourney | $10/thang | Hinh anh chat luong cao | Trung binh |
| RunwayML | $12/thang | Video AI | Thap |
