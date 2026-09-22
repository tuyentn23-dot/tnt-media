import os
import logging
from PIL import Image, ImageDraw, ImageFont

logging.basicConfig(
    filename='output/viral_manager.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def generate_high_ctr_thumbnail(title_text, output_path="output/thumbnail.jpg"):
    """
    Mô-đun tự động tạo thumbnail / bìa video có độ tương phản cao (High-CTR Thumbnail Generator)
    nhằm tối đa hóa tỷ lệ nhấp chuột (CTR) cho các video Shorts trên YouTube.
    """
    print(f"[Thumbnail Generator] Đang thiết kế bìa video chuẩn CTR cao cho: {title_text}")
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    # Tạo khung hình kích thước chuẩn dọc 9:16 (1080x1920)
    width, height = 1080, 1920
    image = Image.new("RGB", (width, height), color=(15, 23, 42))
    draw = ImageDraw.Draw(image)
    
    # Vẽ hiệu ứng gradient / khối màu nền nổi bật
    draw.rectangle([50, 50, width - 50, height - 50], outline=(59, 130, 246), width=8)
    
    # Vẽ tiêu đề nổi bật
    try:
        # Cố gắng sử dụng font hệ thống
        font = ImageFont.truetype("arial.ttf", 70)
    except IOError:
        font = ImageFont.load_default()
        
    # Định dạng văn bản ngắt dòng đơn giản
    text_y = 800
    draw.text((100, text_y), "🔥 HOT TREND AI", fill=(239, 68, 68), font=font)
    draw.text((100, text_y + 100), title_text[:40] + "...", fill=(255, 255, 255), font=font)
    
    image.save(output_path, "JPEG")
    print(f"[Thumbnail Generator] Đã tạo thành công bìa video tại: {output_path}")
    logging.info(f"High-CTR thumbnail generated successfully: {output_path}")
    return output_path
