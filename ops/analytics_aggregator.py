import json
import os
import logging

logging.basicConfig(
    filename='output/viral_manager.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

class AnalyticsAggregator:
    """
    Mô-đun tổng hợp và phân tích dữ liệu vĩ mô (Analytics Aggregator & Macro Strategist).
    Tự động đọc toàn bộ lịch sử xuất bản và số liệu PDCA để đưa ra quyết định chiến lược
    về chủ đề, tốc độ đăng và phân khúc khán giả tối ưu cho kênh 24/7.
    """
    def __init__(self, history_path="output/pdca_history.json"):
        self.history_path = history_path

    def aggregate_and_decide(self):
        print("[Analytics Aggregator] Đang tổng hợp toàn bộ dữ liệu vĩ mô từ lịch sử chu kỳ PDCA...")
        if not os.path.exists(self.history_path):
            return {"strategy_mode": "Growth", "boost_factor": 1.0}
            
        try:
            with open(self.history_path, "r", encoding="utf-8") as f:
                history = json.load(f)
                
            total_cycles = len(history)
            avg_views = sum(item.get("metrics", {}).get("views", 0) for item in history) / max(total_cycles, 1)
            
            print(f"[Analytics Aggregator] Tổng số chu kỳ đã phân tích: {total_cycles} | Lượng views trung bình: {avg_views:.1f}")
            
            if avg_views > 10000:
                print("[Analytics Aggregator] Kênh đang tăng trưởng mạnh! Kích hoạt chế độ Scale-Up (Tăng tốc độ sản xuất).")
                logging.info("Macro strategy adjusted to Scale-Up mode based on high view velocity.")
                return {"strategy_mode": "Scale-Up", "posting_interval_hours": 4}
            else:
                print("[Analytics Aggregator] Duy trì chế độ tối ưu hóa chất lượng nội dung (Optimization Mode).")
                logging.info("Macro strategy set to Optimization mode.")
                return {"strategy_mode": "Optimization", "posting_interval_hours": 6}
        except Exception as e:
            logging.error(f"Lỗi phân tích vĩ mô: {e}")
            return {"strategy_mode": "Default", "posting_interval_hours": 6}

aggregator = AnalyticsAggregator()
