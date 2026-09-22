import time
import logging
import traceback
from ops.supervisor import autonomous_supervisor
from ops.analytics_aggregator import aggregator
from ops.community_manager import community_manager
from ops.auto_evolution import evolution_engine
from ops.telegram_commander import commander

logging.basicConfig(
    filename='output/viral_manager.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def start_master_orchestrator():
    """
    Master Daemon Orchestrator: Trạm điều khiển trung tâm tối cao.
    Điều phối toàn bộ hệ sinh thái tự động hóa 24/7 gồm Supervisor, Analytics Aggregator,
    Community Manager, Auto Evolution và Telegram Commander.
    """
    print("=================================================================")
    print("🚀 KHỞI ĐỘNG MASTER DAEMON ORCHESTRATOR - VẬN HÀNH 24/7 REAL-TIME")
    print("=================================================================")
    commander.send_alert("👑 Master Daemon Orchestrator đã chính thức kích hoạt toàn quyền vận hành kênh tự động!")
    
    # Kích hoạt chu kỳ tự tiến hóa ban đầu
    evolution_engine.analyze_and_mutate()
    
    # Phân tích chiến lược vĩ mô ban đầu
    macro_strategy = aggregator.aggregate_and_decide()
    print(f"[Orchestrator] Chiến lược vĩ mô hiện tại: {macro_strategy}")
    
    # Chuyển giao quyền điều khiển sang Supervisor Daemon
    try:
        autonomous_supervisor()
    except Exception as e:
        err_msg = f"🔥 Lỗi tối cao tại Master Orchestrator: {str(e)}\n{traceback.format_exc()[-400:]}"
        logging.error(err_msg)
        commander.send_alert(err_msg)

def start_golden_scheduler():
    import threading
    from ops.scheduler import run_forever
    t = threading.Thread(target=run_forever, daemon=True)
    t.start()
    return t


if __name__ == "__main__":
    start_golden_scheduler()
    while True:
        time.sleep(60)
