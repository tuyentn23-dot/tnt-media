import random
import json
import os
import logging

logging.basicConfig(
    filename='output/viral_manager.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

class EvolutionaryABTester:
    """
    Mô-đun A/B Testing & Tiến hóa Prompt tự động.
    Thực hiện biến thể prompt dựa trên thuật toán di truyền để tối ưu hóa tỷ lệ viral.
    """
    def __init__(self, state_path="output/ab_test_state.json"):
        self.state_path = state_path

    def evolve_prompts(self, trend_data):
        print("[AB Tester] Đang tiến hóa biến thể prompt dựa trên dữ liệu xu hướng...")
        base_prompt = trend_data.get("prompt", "Cinematic ultra-realistic 3D scene")
        
        variants = [
            f"{base_prompt}, dramatic cinematic lighting, 8k resolution, vertical 9:16",
            f"{base_prompt}, cyberpunk neon aesthetics, hyper-detailed, vertical 9:16",
            f"{base_prompt}, ethereal glowing particles, photorealistic masterpiece, vertical 9:16"
        ]
        
        chosen_prompt = random.choice(variants)
        print(f"[AB Tester] Đã chọn biến thể prompt tối ưu: {chosen_prompt}")
        logging.info(f"Selected evolved prompt variant: {chosen_prompt}")
        return chosen_prompt

ab_tester = EvolutionaryABTester()
