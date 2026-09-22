import os
import sys
import subprocess
import time
import webbrowser
import logging

if sys.stdout.encoding.lower() != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

logging.basicConfig(
    filename='output/viral_manager.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def run_full_stack():
    print("==========================================================")
    print("🚀 KHỞI ĐỘNG TOÀN BỘ HỆ THỐNG: DASHBOARD + PORT + VIDEO PRODUCTION")
    print("==========================================================")
    
    # 1. Khởi chạy Dashboard Web Server (FastAPI) trên nền sau
    print("\n[1/3] Đang khởi động Web Monitoring Dashboard tại http://127.0.0.1:8000...")
    dashboard_process = subprocess.Popen([sys.executable, "ops/dashboard.py"])
    
    # Chờ 2 giây để server khởi tạo port thành công
    time.sleep(2)
    
    # 2. Tự động mở trình duyệt web đến Dashboard
    print("\n[2/3] Đang mở giao diện Dashboard trên trình duyệt...")
    try:
        webbrowser.open("http://127.0.0.1:8000")
    except Exception as e:
        print(f"Không thể tự động mở trình duyệt: {e}")
        
    # 3. Kích hoạt ngay chu kỳ sản xuất video & tiến hóa PDCA
    print("\n[3/3] Đang thực thi chu kỳ sản xuất video Shorts & vòng lặp PDCA...")
    subprocess.run([sys.executable, "run_once_pdca.py"])
    
    print("\n==========================================================")
    print("✅ HỆ THỐNG ĐÃ SẴN SÀNG: PORT ĐANG MỞ, DASHBOARD ĐANG CHẠY & VIDEO ĐÃ ĐƯỢC XỬ LÝ!")
    print("==========================================================")
    
    # Giữ tiến trình dashboard chạy
    try:
        dashboard_process.wait()
    except KeyboardInterrupt:
        dashboard_process.terminate()

if __name__ == "__main__":
    run_full_stack()
