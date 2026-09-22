
"""
TNT Media v2 - Main Orchestrator
Dieu phoi toan bo pipeline AI YouTube automation
"""

import json
from pathlib import Path
import sys

# Import cac module
sys.path.insert(0, 'tnt_media_v2')
from generators.visualizer_engine import AudioVisualizerEngine
from generators.thumbnail_generator import ThumbnailGenerator
from pipeline.auto_publisher import AutoPublisher

class TNTMediaOrchestrator:
    """Orchestrator chinh cho TNT Media v2"""
    
    def __init__(self, config_path='tnt_media_v2/config/channels_config.json'):
        with open(config_path, 'r', encoding='utf-8') as f:
            self.config = json.load(f)
        
        self.visualizer = AudioVisualizerEngine()
        self.thumbnail_gen = ThumbnailGenerator()
        self.publisher = AutoPublisher()
    
    def produce_music_video(self, audio_path, title, artist, output_dir='tnt_media_v2/output'):
        """San xuat video nhac hoan chinh"""
        print("=" * 50)
        print("TNT MEDIA v2 - SAN XUAT VIDEO NHAC")
        print("=" * 50)
        
        output_dir = Path(output_dir)
        output_dir.mkdir(exist_ok=True, parents=True)
        
        # Buoc 1: Tao visualizer video
        print("
[1/3] Tao visualizer...")
        visual_path = output_dir / 'visualizer.mp4'
        self.visualizer.create_visualizer_video(
            audio_path,
            str(visual_path),
            title,
            artist
        )
        print(f"  Visual: {visual_path}")
        
        # Buoc 2: Tao thumbnail
        print("
[2/3] Tao thumbnail...")
        thumb_path = output_dir / 'thumbnail.jpg'
        self.thumbnail_gen.create_music_thumbnail(
            title,
            artist,
            str(thumb_path)
        )
        print(f"  Thumbnail: {thumb_path}")
        
        # Buoc 3: Ghep audio vao video
        print("
[3/3] Ghep audio...")
        final_path = self._merge_audio(visual_path, audio_path, output_dir)
        print(f"  Final: {final_path}")
        
        return final_path, thumb_path
    
    def _merge_audio(self, visual_path, audio_path, output_dir):
        """Ghep audio vao video bang ffmpeg"""
        import subprocess
        import imageio_ffmpeg
        
        ffmpeg = imageio_ffmpeg.get_ffmpeg_exe()
        final_path = output_dir / 'final_video.mp4'
        
        cmd = [
            ffmpeg,
            '-i', str(visual_path),
            '-i', str(audio_path),
            '-c:v', 'copy',
            '-c:a', 'aac',
            '-b:a', '192k',
            '-shortest',
            '-y',
            str(final_path)
        ]
        
        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode == 0:
            return final_path
        else:
            print(f"Error: {result.stderr[:200]}")
            return visual_path
    
    def publish_music_video(self, video_path, thumb_path, title, description, tags):
        """Dang video len YouTube"""
        print("
Dang video len YouTube...")
        video_id = self.publisher.publish_video(
            str(video_path),
            title,
            description,
            tags
        )
        
        # Dat thumbnail
        self.publisher.set_thumbnail(video_id, str(thumb_path))
        
        return video_id

if __name__ == '__main__':
    orchestrator = TNTMediaOrchestrator()
    
    # San xuat video nhac
    final_video, thumbnail = orchestrator.produce_music_video(
        audio_path='library/Nắng Sớm Trên Vai.wav',
        title='Nang Som Tren Vai',
        artist='TNT Music Studio - Album: Tinh Ca'
    )
    
    print(f"
Video final: {final_video}")
    print(f"Thumbnail: {thumbnail}")
