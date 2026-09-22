import os
import time

def generate_visual(prompt: str, scene_id: int, output_dir="assets/visuals", media_type="image"):
    print(f"[INFO] Bat dau tao {media_type} cho phan canh {scene_id}...")
    os.makedirs(output_dir, exist_ok=True)
    
    api_key = os.getenv("VISUAL_API_KEY")
    filename = f"scene_{scene_id}.{'mp4' if media_type == 'video' else 'png'}"
    filepath = os.path.join(output_dir, filename)
    
    if not api_key:
        print(f"[WARNING] Thieu VISUAL_API_KEY. Tao file {media_type} gia lap cho phan canh {scene_id}.")
        # Tao file dummy de he thong khong bi nghen
        with open(filepath, 'wb') as f:
            f.write(b"dummy visual content")
        return filepath

    # Template goi API (Leonardo / SeaArt / Midjourney qua API wrapper)
    print(f"[INFO] Dang gui prompt toi AI Visual: '{prompt[:50]}...'")
    try:
        # Thuc te: Gui requests.post toi endpoint cua SeaArt hoac Leonardo.ai o day
        # payload = {"prompt": prompt, "model": "sdxl"...}
        time.sleep(2) # Gia lap thoi gian cho API sinh anh
        
        # Ghi file sau khi nhan ket qua
        with open(filepath, 'wb') as f:
            f.write(b"simulated downloaded content")
        print(f"[SUCCESS] Da luu {media_type} tai {filepath}")
        return filepath
    except Exception as e:
        print(f"[ERROR] Loi goi Visual API: {e}")
        with open(filepath, 'wb') as f:
            f.write(b"dummy visual content")
        return filepath

if __name__ == "__main__":
    print("=== TEST VISUAL GENERATOR ===")
    generate_visual("Mot chu meo dang thuyet trinh ve AI, cinematic lighting", 1, media_type="image")
