import sqlite3
import os
import datetime
import logging

logging.basicConfig(
    filename='output/viral_manager.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

class AnalyticsManager:
    def __init__(self, db_path="output/system_analytics.db"):
        self.db_path = db_path
        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
        self._init_database()

    def _init_database(self):
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS video_performance (
                    video_id TEXT PRIMARY KEY,
                    title TEXT,
                    trend_keyword TEXT,
                    genre TEXT,
                    publish_time TIMESTAMP,
                    views INTEGER DEFAULT 0,
                    likes INTEGER DEFAULT 0,
                    performance_score REAL DEFAULT 0.0
                )
            ''')
            conn.commit()
            conn.close()
        except Exception as e:
            logging.error(f"[Analytics DB Error]: {str(e)}")

    def log_published_video(self, video_id, title, trend_keyword, genre):
        if not video_id:
            return
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            publish_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            cursor.execute('''
                INSERT INTO video_performance (video_id, title, trend_keyword, genre, publish_time)
                VALUES (?, ?, ?, ?, ?)
            ''', (video_id, title, trend_keyword, genre, publish_time))
            
            conn.commit()
            conn.close()
            print(f"[Analytics] Đã lưu video {video_id} vào DB để học hỏi.")
        except Exception as e:
            print(f"[Analytics Error]: {str(e)}")

    def sync_youtube_metrics(self, youtube_service):
        """Gọi API YouTube cập nhật lượt view và like thực tế của các video đã đăng."""
        if not youtube_service:
            return
            
        print("[Analytics] Đang đồng bộ hóa dữ liệu lượt xem từ YouTube...")
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            # Chỉ lấy các video thực tế (Bỏ qua MOCK_ID)
            cursor.execute('SELECT video_id FROM video_performance WHERE video_id NOT LIKE "MOCK_%"')
            rows = cursor.fetchall()
            
            if not rows:
                conn.close()
                return
                
            video_ids = [row[0] for row in rows]
            
            # Cập nhật hàng loạt (Mỗi request YouTube hỗ trợ tối đa 50 ID)
            for i in range(0, len(video_ids), 50):
                batch = video_ids[i:i+50]
                request = youtube_service.videos().list(
                    part="statistics",
                    id=",".join(batch)
                )
                response = request.execute()
                
                for item in response.get("items", []):
                    vid = item["id"]
                    stats = item.get("statistics", {})
                    views = int(stats.get("viewCount", 0))
                    likes = int(stats.get("likeCount", 0))
                    
                    cursor.execute('''
                        UPDATE video_performance 
                        SET views = ?, likes = ?, performance_score = ?
                        WHERE video_id = ?
                    ''', (views, likes, views + (likes * 5), vid))
                    
            conn.commit()
            conn.close()
            print("[Analytics] ✅ Đồng bộ dữ liệu thành công! CSDL đã được làm mới với thông số YouTube thực tế.")
        except Exception as e:
            logging.error(f"[Analytics Sync Error]: {str(e)}")

    def get_best_performing_genre(self):
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute('''
                SELECT genre, AVG(views + (likes * 5)) as avg_score 
                FROM video_performance 
                GROUP BY genre 
                ORDER BY avg_score DESC 
                LIMIT 1
            ''')
            result = cursor.fetchone()
            conn.close()
            
            if result and result[0]:
                return result[0]
            return "Cyber Phonk Energy"
        except Exception as e:
            return "Cyber Phonk Energy"

analytics_manager = AnalyticsManager()
