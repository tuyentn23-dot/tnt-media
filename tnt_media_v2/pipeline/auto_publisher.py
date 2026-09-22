
"""
TNT Media v2 - Auto Publisher
Tu dong dang video len YouTube voi SEO toi uu
"""

import pickle
from pathlib import Path
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
import json

class AutoPublisher:
    """Tu dong dang video len YouTube"""
    
    def __init__(self, token_path='token.pickle'):
        with open(token_path, 'rb') as f:
            credentials = pickle.load(f)
        self.youtube = build('youtube', 'v3', credentials=credentials)
        self.memory_file = Path('memory/published_videos.json')
    
    def publish_video(self, video_path, title, description, tags, category_id='10', privacy='public'):
        """Dang video len YouTube"""
        body = {
            'snippet': {
                'title': title,
                'description': description,
                'tags': tags,
                'categoryId': category_id
            },
            'status': {
                'privacyStatus': privacy,
                'selfDeclaredMadeForKids': False
            }
        }
        
        media = MediaFileUpload(
            video_path,
            mimetype='video/mp4',
            resumable=True,
            chunksize=1024*1024
        )
        
        request = self.youtube.videos().insert(
            part='snippet,status',
            body=body,
            media_body=media
        )
        
        response = None
        while response is None:
            status, response = request.next_chunk()
        
        self._save_to_memory(response['id'], title)
        return response['id']
    
    def set_thumbnail(self, video_id, thumbnail_path):
        """Dat thumbnail cho video"""
        self.youtube.thumbnails().set(
            videoId=video_id,
            media_body=MediaFileUpload(thumbnail_path)
        ).execute()
        print(f"Thumbnail set for video {video_id}")
    
    def _save_to_memory(self, video_id, title):
        """Luu thong tin video da dang"""
        if self.memory_file.exists():
            with open(self.memory_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
        else:
            data = {'videos': []}
        
        data['videos'].append({'id': video_id, 'title': title})
        
        with open(self.memory_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
