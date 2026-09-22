import os

def generate_srt(script_text: str, srt_path: str = "assets/subtitles.srt") -> str:
    os.makedirs(os.path.dirname(srt_path), exist_ok=True)
    print(f"[INFO] Dang tao file phu de (.srt) tu kich ban...")
    
    # Chia kịch bản thành các câu hoặc các đoạn nhỏ mỗi đoạn khoảng 50-80 ký tự
    words = script_text.split()
    chunks = []
    current_chunk = []
    for word in words:
        current_chunk.append(word)
        if len(" ".join(current_chunk)) > 40:
            chunks.append(" ".join(current_chunk))
            current_chunk = []
    if current_chunk:
        chunks.append(" ".join(current_chunk))
        
    srt_lines = []
    duration_per_chunk = 4.0 # Giả định mỗi đoạn hiển thị 4 giây
    
    def format_time(seconds):
        hours = int(seconds // 3600)
        minutes = int((seconds % 3600) // 60)
        secs = int(seconds % 60)
        millisecs = int((seconds - int(seconds)) * 1000)
        return f"{hours:02d}:{minutes:02d}:{secs:02d},{millisecs:03d}"
        
    start_time = 0.0
    for i, chunk in enumerate(chunks[:10], start=1): # Lấy tối đa 10 dòng đầu cho video ngắn
        end_time = start_time + duration_per_chunk
        srt_lines.append(str(i))
        srt_lines.append(f"{format_time(start_time)} --> {format_time(end_time)}")
        srt_lines.append(chunk)
        srt_lines.append("")
        start_time = end_time
        
    with open(srt_path, "w", encoding="utf-8") as f:
        f.write("\n".join(srt_lines))
        
    print(f"[SUCCESS] Da tao file phu de tai: {srt_path}")
    return srt_path
