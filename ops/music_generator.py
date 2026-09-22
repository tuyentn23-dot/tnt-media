import os
import logging
import random

logging.basicConfig(
    filename='output/viral_manager.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

class ProTrendMusicComposer:
    """
    Mô-đun sáng tác nhạc và lời bài hát chuyên nghiệp theo chuẩn xu hướng ngắn (TikTok / YouTube Shorts).
    Tập trung vào vần điệu, nhịp phách dồn dập, cấu trúc Hook - Verse - Drop bắt tai và cảm xúc.
    """
    def __init__(self, output_dir="output/audio"):
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)
        
        self.trend_song_templates = {
            "Cyber Phonk Energy": [
                (
                    "Đêm buông xuống, ánh đèn neon lóe lên trong màn sương!\n"
                    "Tốc độ tăng dần, không một ai có thể ngăn đường ta bước!\n"
                    "Cháy hết mình hôm nay, đạp bằng mọi chông gai trước mắt,\n"
                    "Bật chế độ săn tiền, vươn lên đỉnh cao thế giới này! Oh-oh!"
                ),
                (
                    "Nhìn thẳng vào tương lai, dòng thời gian đang trôi vội vã!\n"
                    "Đừng cúi đầu trước khó khăn, hãy để bản lĩnh lên tiếng đi nào!\n"
                    "Phonk beat vang lên, máu trong tim sục sôi từng nhịp đập,\n"
                    "Kẻ chiến thắng là người dám đi đến tận cùng giới hạn!"
                )
            ],
            "Emotional Chill Lo-Fi": [
                (
                    "Giữa thành phố hoài niệm, ta tìm lại chính mình qua từng phím đàn...\n"
                    "Có những nỗi buồn thoáng qua như cơn mưa chiều ngập tràn.\n"
                    "Nhưng ngày mai trời lại sáng, nụ cười trên môi sẽ ở lại,\n"
                    "Vì cuộc đời là những chuyến đi tìm về nơi bình yên nhất."
                ),
                (
                    "Lặng nghe tiếng gió thì thầm qua ô cửa sổ nhỏ...\n"
                    "Những ký ức cũ gác lại, nhường chỗ cho ước mơ đang chờ.\n"
                    "Tự nhủ lòng phải mạnh mẽ qua từng giọt cà phê đắng ngắt,\n"
                    "Rồi mọi chuyện sẽ ổn thôi, ánh sáng cuối đường đang đợi ta."
                )
            ],
            "Catchy GenZ Vibe": [
                (
                    "Lướt qua khung hình, thấy thế giới hôm nay quá ư là lung linh!\n"
                    "Mỗi bước chân đi qua là một dấu ấn riêng không lẫn vào đâu.\n"
                    "Thích là làm, ngại gì ánh mắt của ai xung quanh nói ngả nói nghiêng,\n"
                    "Tuổi trẻ này chỉ có một, tội gì không tỏa sáng rực rỡ hết mình!"
                ),
                (
                    "Alo! Đã đến giờ bật tung năng lượng rồi bạn ơi!\n"
                    "Gạt hết muộn phiền sang bên, cùng nhau bước vào cuộc chơi.\n"
                    "Tụi mình sinh ra đâu phải để sống một đời nhạt nhòa,\nHãy cứ bay cao theo cách mà trái tim bạn đang truyền cảm hứng!"
                )
            ]
        }

    def compose_hit_song(self, custom_theme=None, preferred_genre="Cyber Phonk Energy"):
        print(f"[Music Composer] Đang phân tích xu hướng và sáng tác bài hát thể loại: [{preferred_genre}]...")
        
        if preferred_genre in self.trend_song_templates:
            templates = self.trend_song_templates[preferred_genre]
            raw_lyrics = random.choice(templates)
        else:
            raw_lyrics = random.choice(self.trend_song_templates["Cyber Phonk Energy"])
            
        if custom_theme:
            raw_lyrics = f"Chủ đề: {custom_theme}\n" + raw_lyrics

        print(f"\n--- 🎶 LỜI BÀI HÁT HIT-TREND ĐÃ SÁNG TÁC ---\n{raw_lyrics}\n---------------------------------------------\n")
        
        output_path = os.path.join(self.output_dir, "master_voiceover.mp3")
        
        try:
            from gtts import gTTS
            from moviepy.editor import AudioFileClip
            
            formatted_lyrics = raw_lyrics.replace("\n", ". ... ")
            audio_text = f"🎵 [{preferred_genre}]. {formatted_lyrics}"
            
            temp_path = os.path.join(self.output_dir, "temp_hit_audio.mp3")
            tts = gTTS(text=audio_text, lang='vi', slow=False)
            tts.save(temp_path)
            
            audio_clip = AudioFileClip(temp_path)
            audio_clip.write_audiofile(
                output_path,
                fps=44100,
                nbytes=2,
                codec='libmp3lame',
                logger=None
            )
            
            audio_clip.close()
            if os.path.exists(temp_path):
                os.remove(temp_path)
                
            print(f"[Music Composer] Đã sản xuất file âm thanh hit-trend thành công tại: {output_path}")
            return output_path
            
        except Exception as e:
            err_msg = f"[Music Composer Error]: {str(e)}"
            print(err_msg)
            logging.error(err_msg)
            return None

pro_trend_music_composer = ProTrendMusicComposer()
