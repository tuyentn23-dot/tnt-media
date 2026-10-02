import time
import subprocess
import sys

def run_pipeline_job():
    print("\n[SCHEDULER] Bat dau chay lich trinh san xuat video tu dong...")
    subprocess.run([sys.executable, "main_pipeline.py"])

def start_scheduler():
    print("[INFO] He thong tu dong lich chay (Scheduler) da duoc khoi dong.")
    print("[INFO] De test ngay lap tuc, dang thuc thi 1 chu ky dau tien...")
    run_pipeline_job()
    
    # Vi du thiet lap chay dinh ky (chay moi 24 gio hoac theo khung gio yeu cau)
    # import schedule
    # schedule.every().day.at("08:00").do(run_pipeline_job)
    # while True:
    #     schedule.run_pending()
    #     time.sleep(1)

if __name__ == "__main__":
    start_scheduler()
