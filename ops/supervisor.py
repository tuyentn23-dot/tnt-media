import time
import logging
import traceback
from ops.state_manager import state_manager
from ops.telegram_commander import commander
from auto_publisher import main as run_pdca_cycle

logging.basicConfig(
    filename='output/viral_manager.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def autonomous_supervisor():
    """
    Hệ thống giám sát tự động 24/7 (Supervisor Daemon). 
    Tự động bắt lỗi, gửi cảnh báo qua Telegram và tự phục hồi hệ thống khi có sự cố xảy ra.
    """
    print("[Supervisor] Khởi động hệ thống giám sát tự động kênh YouTube Shorts 24/7...")
    commander.send_alert("🚀 Hệ thống tự động hóa YouTube Shorts đã khởi động và sẵn sàng vận hành 24/7!")
    
    cycle_count = 0
    while True:
        cycle_count += 1
        print(f"\n[Supervisor] === BẮT ĐẦU CHU KỲ PDCA # {cycle_count} ===")
        try:
            run_pdca_cycle()
            state_manager.state["total_videos_published"] += 1
            state_manager.save_state()
            
            success_msg = f"✅ Chu kỳ PDCA #{cycle_count} hoàn tất thành công! Tổng video đã xuất bản: {state_manager.state['total_videos_published']}"
            print(f"[Supervisor] {success_msg}")
            commander.send_alert(success_msg)
            
        except Exception as e:
            err_msg = f"❌ CẢNH BÁO LỖI trong chu kỳ #{cycle_count}: {str(e)}\n\nTraceback:\n{traceback.format_exc()[-500:]}"
            logging.error(err_msg)
            print(f"[Supervisor Error]: {e}")
            commander.send_alert(err_msg)
            
            print("[Supervisor] Đang chờ 60 giây trước khi tự động khởi động lại chu kỳ để đảm bảo tính liên tục...")
            time.sleep(60)
            continue
            
        # Nghỉ 6 giờ trước chu kỳ tiếp theo để tối ưu hóa thuật toán đề xuất của YouTube
        print("[Supervisor] Đang chuyển sang trạng thái chờ chu kỳ tiếp theo (6 giờ)... Telegram sẵn sàng nhận lệnh.")
        for _ in range(21600):
            # Kiểm tra lệnh điều khiển từ xa qua Telegram mỗi 10 giây
            commands = commander.poll_commands()
            for cmd in commands:
                if "/run_now" in cmd:
                    commander.send_alert("⚡ Nhận lệnh kích hoạt khẩn cấp từ người vận hành! Bắt đầu ngay chu kỳ mới...")
                    break
            else:
                time.sleep(10)
                continue
            break

if __name__ == "__main__":
    autonomous_supervisor()
