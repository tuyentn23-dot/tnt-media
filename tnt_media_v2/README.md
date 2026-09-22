# TNT MEDIA v2 - AI YouTube Automation System

## Gioi thieu
TNT Media v2 la he thong AI tu dong san xuat va dang video YouTube chat luong cao.
Duoc xay dung dua tren nghien cuu cac kenh YouTube AI thanh cong.

## Kien truc

```
tnt_media_v2/
├── agents/
│   └── (Research, Script, SEO agents)
├── generators/
│   ├── visualizer_engine.py      # Audio Visualizer
│   ├── thumbnail_generator.py    # Thumbnail chuyen nghiep
│   └── (Future: AI image, video)
├── pipeline/
│   ├── orchestrator.py           # Main orchestrator
│   ├── auto_publisher.py         # Tu dong dang YouTube
│   └── (Future: quality checker)
├── config/
│   └── channels_config.json      # Cau hinh kenh
└── output/
    ├── videos/
    ├── thumbnails/
    └── analytics/
```

## Thanh phan da hoan thanh

### 1. Audio Visualizer Engine
- Phan tich audio thanh spectrum data
- Tao video visualizer dong bo voi am nhac
- Spectrum bars voi mau sac gradient
- Ho tro bat ky audio WAV/MP3

### 2. Thumbnail Generator
- Tao thumbnail chuyen nghiep
- Co bieu tuong am nhac
- Text ro rang, mau sac noi bat

### 3. Auto Publisher
- Tu dong dang video len YouTube
- Tao metadata SEO toi uu
- Dat thumbnail cho video

### 4. Main Orchestrator
- Dieu phoi toan bo pipeline
- San xuat video nhac hoan chinh
- Ghep audio bang FFmpeg

## Cach su dung

```bash
# Chay orchestrator
cd tnt_media_v2
python pipeline/orchestrator.py
```

## Pipeline hien tai

```
Audio File → Analyze → Visualizer → Merge Audio → Thumbnail → Publish
```

## Pipeline tuong lai (Phase 2+)

```
Topic → Script AI → Voice AI → Music AI → Visual AI → Composite → SEO → Publish → Analytics
```

## Cong nghe su dung

- OpenCV: Xu ly video
- NumPy: Xu ly du lieu
- FFmpeg: Ghep audio/video
- Google YouTube API: Dang video
- Wave: Doc audio

## Cac buoc tiep theo

1. Tich hop Bark AI cho giong noi tieng Viet
2. Tich hop Stable Diffusion cho hinh anh AI
3. Tao Research Agent de tim nich
4. Tao Quality Checker de dam bao chat luong
5. Tao Analytics Dashboard de theo doi hieu suat
