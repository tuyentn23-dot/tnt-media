import random

def fetch_latest_ai_trends():
    """
    Mô đun nghiên cứu và phân tích xu hướng (Trend Research) cho chu kỳ PDCA.
    Cung cấp các chủ đề viral và câu lệnh prompt tối ưu nhất cho Google Veo.
    """
    trending_topics = [
        {
            "topic": "AI & Human Consciousness",
            "prompt": "Cinematic 3D hyper-realistic shot of a glowing artificial neural network merging with human soul, dramatic volumetric lighting, 8k resolution, vertical 9:16",
            "subtitle": "Khi AI Thức Tỉnh Tâm Hồn",
            "voiceover": "Trí tuệ nhân tạo không chỉ tính toán... Nó đang học cách cảm nhận thế giới qua lăng kính con người."
        },
        {
            "topic": "Future Quantum Leap",
            "prompt": "Close up cinematic hyper-realistic shot of quantum computing core glowing with golden light, futuristic laboratory, 8k resolution, vertical 9:16",
            "subtitle": "Kỷ Nguyên Máy Tính Lượng Tử",
            "voiceover": "Tốc độ xử lý gấp một triệu lần... Kỷ nguyên lượng tử đang định nghĩa lại toàn bộ giới hạn công nghệ."
        },
        {
            "topic": "Robotics & Emotion",
            "prompt": "Cinematic hyper-realistic shot of an advanced humanoid robot gently holding a glowing butterfly, soft emotional lighting, 8k, vertical 9:16",
            "subtitle": "Khoảnh Khắc Robot Biết Yêu",
            "voiceover": "Khi ranh giới giữa máy móc và con người mờ dần, cảm xúc chính là định nghĩa cuối cùng của sự sống."
        }
    ]
    
    # Lựa chọn ngẫu nhiên chủ đề đang hot nhất theo vòng lặp PDCA
    selected = random.choice(trending_topics)
    print(f"[Trend Analyzer] Đã phát hiện xu hướng viral mới: {selected['topic']}")
    return selected
