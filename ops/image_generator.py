import os
import subprocess
import requests

def generate_ai_visual(prompt_text: str, output_path: str = "assets/background_image.png") -> str:
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    print(f"[INFO] Dang tao hinh anh minh hoa bang AI cho prompt: {prompt_text[:50]}...")
    
    # Thử kết nối Local Stable Diffusion WebUI / ComfyUI API (port mặc định 7860)
    sd_url = "http://127.0.0.1:7860/sdapi/v1/txt2img"
    payload = {
        "prompt": prompt_text,
        "steps": 20,
        "width": 720,
        "height": 1280,
        "cfg_scale": 7.0
    }
    
    try:
        response = requests.post(sd_url, json=payload, timeout=5)
        if response.status_code == 200:
            r_json = response.json()
            import base64
            img_data = base64.b64decode(r_json["images"][0])
            with open(output_path, "wb") as f:
                f.write(img_data)
            print(f"[SUCCESS] Da tao anh thanh cong qua Stable Diffusion API: {output_path}")
            return output_path
    except Exception as e:
        print(f"[WARNING] Khong ket noi duoc Stable Diffusion local ({e}), chuyen sang tao frame mau dong bang FFmpeg...")
        
    # Fallback: Tạo video nền chuyển động hoặc ảnh động bằng FFmpeg
    subprocess.run([
        "ffmpeg", "-y", "-f", "lavfi", "-i", "color=c=darkblue:s=720x1280:d=6",
        "-c:v", "libx264", "-pix_fmt", "yuv420p", "assets/base_video.mp4"
    ], capture_output=True)
    print(f"[INFO] Da khoi tao video nen dong tu FFmpeg.")
    return "assets/base_video.mp4"
