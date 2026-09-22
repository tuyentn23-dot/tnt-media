import time
import subprocess
import sys
import logging
import datetime
from ops.telegram_commander import commander

logging.basicConfig(
    filename='output/viral_manager.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def start_watchdog():
    """
    System Watchdog & Process Guard:
    Giám sát tiến trình Master Daemon 24/7. Nếu xảy ra sự cố sập nguồn/lỗi tiến trình,
    Watchdog sẽ tự động khởi động lại hệ thống và gửi thông báo khẩn cấp qua Telegram.
    """
    print("[Watchdog] Khởi động hệ thống giám sát tiến trình Watchdog 24/7...")
    commander.send_alert("🛡️ Watchdog System đã kích hoạt bảo vệ toàn diện tiến trình tự động hóa YouTube Shorts!")
    
    while True:
        start_time = datetime.datetime.now()
        print(f"[Watchdog] Đang khởi chạy Master Daemon Orchestrator lúc {start_time}...")
        
        process = subprocess.Popen([sys.executable, "ops/master_daemon_orchestrator.py"])
        
        # Chờ tiến trình chạy
        exit_code = process.wait()
        
        end_time = datetime.datetime.now()
        duration = (end_time - start_time).total_seconds()
        
        warning_msg = f"⚠️ Master Daemon đã dừng lại với exit code {exit_code} sau {duration:.1f} giây. Watchdog đang tự động khởi động lại..."
        print(f"[Watchdog] {warning_msg}")
        logging.warning(warning_msg)
        commander.send_alert(warning_msg)
        
        # Chờ 10 giây trước khi restart để tránh lặp vô hạn lỗi liên tục
        time.sleep(10)

if __name__ == "__main__":
    start_watchdog()
