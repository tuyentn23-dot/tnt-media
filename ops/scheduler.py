import os
import time
try:
    import schedule
except ImportError:
    print("[WARNING] Thu vien 'schedule' chua duoc cai dat. Vui long chay: pip install schedule")
    schedule = None

def job():
    print("
" + "="*50)
    print("⏰ [SCHEDULER] KICH HOAT DAY CHUYEN SAN XUAT TU DONG!")
    print("="*50)
    # Chay file main_pipeline.py trong moi truong doc lap
    os.system("python main_pipeline.py")

def run_scheduler(run_time="20:00"):
    if not schedule:
        print("[ERROR] Khong the chay Scheduler do thieu thu vien.")
        return
        
    print(f"[INFO] He thong da len lich chay tu dong vao {run_time} moi ngay.")
    schedule.every().day.at(run_time).do(job)
    
    print("[INFO] Scheduler dang chay ngam... (An Ctrl+C de thoat)")
    while True:
        schedule.run_pending()
        time.sleep(60) # Kiem tra 1 phut 1 lan

if __name__ == '__main__':
    # Mac dinh hen 8h toi moi ngay, ban co the doi trong thuc te
    run_scheduler("20:00")
