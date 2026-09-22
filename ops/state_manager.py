import os
import json
import datetime

class StateManager:
    """
    Quản lý trạng thái và cơ sở dữ liệu cục bộ cho hệ thống tự động hóa 24/7.
    Lưu trữ lịch sử video đã xuất bản, trạng thái chu kỳ PDCA và số liệu thống kê.
    """
    def __init__(self, db_path="output/system_state.json"):
        self.db_path = db_path
        self.load_state()

    def load_state(self):
        if os.path.exists(self.db_path):
            try:
                with open(self.db_path, "r", encoding="utf-8") as f:
                    self.state = json.load(f)
            except Exception:
                self.state = {"total_videos_published": 0, "history": []}
        else:
            self.state = {"total_videos_published": 0, "history": []}

    def save_state(self):
        os.makedirs("output", exist_ok=True)
        with open(self.db_path, "w", encoding="utf-8") as f:
            json.dump(self.state, f, ensure_ascii=False, indent=4)

    def record_publication(self, video_id, title, metrics):
        self.state["total_videos_published"] += 1
        record = {
            "index": self.state["total_videos_published"],
            "video_id": video_id,
            "title": title,
            "timestamp": datetime.datetime.now().isoformat(),
            "metrics": metrics
        }
        self.state["history"].append(record)
        self.save_state()

state_manager = StateManager()
