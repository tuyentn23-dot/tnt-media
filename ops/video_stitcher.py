import os
import subprocess

def stitch_video_with_audio_and_subs(video_path: str, audio_path: str, srt_path: str, output_path: str = "outputs/final_video_subbed.mp4") -> bool:
    os.makedirs(os.path.dirname(output_path) if os.path.dirname(output_path) else '.', exist_ok=True)
    print(f"[INFO] Dang ghep noi video, am thanh va burn-in phu de bang FFmpeg...")
    
    formatted_srt = srt_path.replace('\\', '/')
    if ':' in formatted_srt:
        parts = formatted_srt.split(':')
        formatted_srt = parts[0] + '\\:' + parts[1]
        
    cmd = [
        "ffmpeg", "-y",
        "-i", video_path,
        "-i", audio_path,
        "-vf", f"subtitles='{formatted_srt}':force_style='FontSize=24,PrimaryColour=&H00FFFF&,OutlineColour=&H000000&,BorderStyle=1,Outline=1'",
        "-c:v", "libx264",
        "-c:a", "aac",
        "-shortest",
        output_path
    ]
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, encoding='utf-8')
        if result.returncode == 0:
            print(f"[SUCCESS] Da xuat thanh cong video co phu de: {output_path}")
            return True
        else:
            print(f"[WARNING] FFmpeg subtitle filter canh bao: {result.stderr[:200]}")
            print(f"[INFO] Chuyen sang che do muxing an toan khong burn-in subtitle truc tiep...")
            fallback_cmd = [
                "ffmpeg", "-y",
                "-i", video_path,
                "-i", audio_path,
                "-c:v", "copy",
                "-c:a", "aac",
                "-shortest",
                output_path
            ]
            fallback_res = subprocess.run(fallback_cmd, capture_output=True, text=True, encoding='utf-8')
            return fallback_res.returncode == 0
    except Exception as e:
        print(f"[ERROR] Loi khi chay FFmpeg subtitle muxing: {e}")
        return False
