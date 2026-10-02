import os
from ops.trend_researcher import research_trend
from ops.script_agents import generate_script
from ops.tts_generator import generate_voiceover
from ops.subtitle_generator import generate_srt
from ops.video_stitcher import stitch_video_with_audio_and_subs

NICHE_TOPICS = [
    "Cong nghe AI va Tu dong hoa",
    "Xu huong Kien truc va Khong gian thong minh",
    "Giai phap Quan ly va Van hanh Doanh nghiep",
    "Chuyen doi So va Cong nghệ 2026"
]

def run():
    print("="*50)
    print("BAT DAU DAY CHUYEN SAN XUAT VIDEO TU DONG (FULL PIPELINE + SUBS)")
    print("="*50)
    
    niche = NICHE_TOPICS[0]
    
    # Phase 1: Research
    print(f"\n--- [PHASE 1] RESEARCH ---")
    topic = research_trend(niche)
    
    # Phase 2: Scripting
    print(f"\n--- [PHASE 2] SCRIPTING ---")
    script = generate_script(topic)
    print(f"[SUCCESS] Noi dung kich ban: {script[:150]}...")
    
    # Phase 3: Voiceover (TTS)
    print(f"\n--- [PHASE 3] VOICE-OVER (TTS) ---")
    audio_file = generate_voiceover(script, "assets/voiceover.mp3")
    
    # Phase 3.5: Subtitles (.srt)
    print(f"\n--- [PHASE 3.5] SUBTITLES GENERATION ---")
    srt_file = generate_srt(script, "assets/subtitles.srt")
    
    # Phase 4: Video Stitching & Subtitle Burn-in
    print(f"\n--- [PHASE 4] VIDEO MUXING & SUBTITLE BURN-IN ---")
    dummy_video = "assets/base_video.mp4"
    if not os.path.exists(dummy_video):
        os.makedirs("assets", exist_ok=True)
        subprocess.run([
            "ffmpeg", "-y", "-f", "lavfi", "-i", "color=c=blue:s=720x1280:d=6", 
            "-c:v", "libx264", "-pix_fmt", "yuv420p", dummy_video
        ], capture_output=True)
        
    output_video = "outputs/final_video_with_subs.mp4"
    os.makedirs("outputs", exist_ok=True)
    success = stitch_video_with_audio_and_subs(dummy_video, audio_file, srt_file, output_video)
    
    if success:
        print(f"\n[SUCCESS] HOAN TAT! Video co phu de da san sang tai: {output_video}")
    else:
        print(f"\n[WARNING] Hoan tat quy trinh voi file du phong.")

if __name__ == "__main__":
    run()
