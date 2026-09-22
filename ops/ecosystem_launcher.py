import os
import sys
import subprocess
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

def launch_autonomous_ecosystem():
    print("==========================================================")
    print("👑 KHỞI ĐỘNG HỆ THỐNG TỰ ĐỘNG HÓA 24/7 HOÀN TOÀN (FULL AUTONOMOUS)")
    print("==========================================================")
    
    # 1. Thực thi ngay một chu kỳ PDCA và tiến hóa đầu tiên
    print("\n[Launcher] Đang thực thi chu kỳ PDCA và tiến hóa khởi đầu...")
    subprocess.run([sys.executable, "run_once_pdca.py"])
    
    # 2. Kích hoạt Watchdog & Master Daemon chạy ngầm liên tục 24/7
    print("\n[Launcher] Kích hoạt Watchdog và Master Orchestrator chạy liên tục 24/7...")
    print("[Launcher] Hệ thống đã chuyển sang chế độ tự trị hoàn toàn. Không cần sự can thiệp thủ công.")
    
    os.execv(sys.executable, [sys.executable, "ops/watchdog.py"])

if __name__ == "__main__":
    launch_autonomous_ecosystem()
