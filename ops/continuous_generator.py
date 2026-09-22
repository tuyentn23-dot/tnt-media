import time
import subprocess
import sys
import logging
import datetime

logging.basicConfig(
    filename='output/viral_manager.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def run_continuous_pipeline(interval_hours=4):
    """
    Vòng lặp sản xuất video tự động 24/7 (Continuous Autonomous Generator).
    Thực hiện liên tục chu kỳ PDCA, tiến hóa prompt, render video qua Google Veo
    và xuất bản theo khoảng thời gian cấu hình sẵn.
    """
    print("==========================================================")
    print("🔄 KÍCH HOẠT VÒNG LẶP SẢN XUẤT VIDEO TỰ ĐỘNG LIÊN TỤC (24/7)")
    print("==========================================================")
    logging.info("Continuous autonomous generator loop started.")
    
    cycle_count = 1
    while True:
        start_time = datetime.datetime.now()
        print(f"\n----------------------------------------------------------")
        print(f"🎬 [Chu kỳ #{cycle_count}] Bắt đầu sản xuất video Shorts lúc: {start_time}")
        print(f"----------------------------------------------------------")
        
        try:
            # Gọi trực tiếp kịch bản chạy một chu kỳ PDCA
            result = subprocess.run([sys.executable, "run_once_pdca.py"], capture_output=True, text=True, encoding="utf-8")
            
            if result.returncode == 0:
                print(f"[Chu kỳ #{cycle_count}] Hoàn tất xuất bản video Shorts thành công!")
                logging.info(f"PDCA Cycle #{cycle_count} completed successfully.")
            else:
                print(f"[Cảnh báo Chu kỳ #{cycle_count}] Có lỗi xảy ra trong quá trình chạy:")
                print(result.stderr)
                logging.error(f"PDCA Cycle #{cycle_count} encountered errors: {result.stderr}")
                
        except Exception as e:
            err_msg = f"Lỗi ngoại lệ tại chu kỳ #{cycle_count}: {str(e)}"
            print(err_msg)
            logging.error(err_msg)
            
        # Tính toán thời gian chờ cho chu kỳ tiếp theo
        wait_seconds = interval_hours * 3600
        next_run_time = datetime.datetime.now() + datetime.timedelta(seconds=wait_seconds)
        print(f"\n⏳ Đã xong chu kỳ #{cycle_count}. Hệ thống sẽ nghỉ ngơi và tiếp tục chu kỳ tiếp theo vào lúc: {next_run_time.strftime('%Y-%m-%d %H:%M:%S')}")
        
        cycle_count += 1
        time.sleep(wait_seconds)

if __name__ == "__main__":
    # Mặc định chạy liên tục mỗi 4 tiếng một video mới
    run_continuous_pipeline(interval_hours=4)
