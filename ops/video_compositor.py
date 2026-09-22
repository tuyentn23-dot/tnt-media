import os
import logging
from moviepy.editor import VideoFileClip, AudioFileClip
from moviepy.video.fx.all import loop

logging.basicConfig(
    filename='output/viral_manager.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def compose_cinematic_video(clip_data_list, voiceover_path, output_path="output/final_master_short.mp4"):
    print("[Compositor] Đang nâng cấp và tổng hợp Master Video chất lượng cao (High-Fidelity)...")
    try:
        if not clip_data_list or not voiceover_path:
            print("[Compositor Error] Thiếu dữ liệu đầu vào (Hình ảnh hoặc Âm thanh).")
            return None
            
        # 1. Nạp âm thanh Master
        audio = AudioFileClip(voiceover_path)
        target_duration = audio.duration
        
        # 2. Nạp hình ảnh Cinematic
        scene_path, _ = clip_data_list[0]
        video = VideoFileClip(scene_path)
        
        # 3. Đồng bộ hóa thời lượng hình ảnh khớp 100% với âm nhạc
        if video.duration < target_duration:
            video = loop(video, duration=target_duration)
        else:
            video = video.subclip(0, target_duration)
            
        # 4. Gắn âm thanh vào video
        video = video.set_audio(audio)
        
        # 5. Kết xuất với tiêu chuẩn phát sóng chất lượng cao
        video.write_videofile(
            output_path,
            fps=30,
            codec="libx264",
            audio_codec="aac",
            preset="medium",
            bitrate="5000k",
            ffmpeg_params=["-pix_fmt", "yuv420p"],
            logger=None
        )
        
        video.close()
        audio.close()
        
        print(f"[Compositor] Tổng hợp Master Video chất lượng cao thành công tại: {output_path}")
        return output_path
        
    except Exception as e:
        err_msg = f"[Compositor Error]: {str(e)}"
        print(err_msg)
        logging.error(err_msg)
        return None
