import os
import json
from datetime import datetime

try:
    from fastapi import FastAPI, HTTPException
    from fastapi.responses import HTMLResponse
    FASTAPI_AVAILABLE = True
except ImportError:
    FASTAPI_AVAILABLE = False

app = FastAPI(title="Venture Foundry - Autonomous YouTube Shorts Dashboard", version="2.0.0")

def load_json_safely(path):
    if os.path.exists(path):
        try:
            with open(path, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return {}
    return {}

@app.get("/", response_class=HTMLResponse)
def read_root():
    state = load_json_safely("output/system_state.json")
    history = load_json_safely("output/pdca_history.json")
    evolution = load_json_safely("output/evolution_state.json")
    
    total_videos = state.get("total_videos_published", 0)
    
    html_content = f"""
    <!DOCTYPE html>
    <html lang="vi">
    <head>
        <meta charset="UTF-8">
        <title>Venture Foundry - Autonomous Dashboard</title>
        <style>
            body {{ background-color: #0f172a; color: #f8fafc; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; margin: 0; padding: 40px; }}
            .container {{ max-width: 1000px; margin: 0 auto; }}
            .header {{ display: flex; justify-content: space-between; align-items: center; border-bottom: 2px solid #334155; padding-bottom: 20px; }}
            .card-grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: 20px; margin-top: 30px; }}
            .card {{ background-color: #1e293b; border-radius: 12px; padding: 25px; box-shadow: 0 4px 6px rgba(0,0,0,0.3); border: 1px solid #334155; }}
            .card h3 {{ margin-top: 0; color: #38bdf8; }}
            .metric {{ font-size: 32px; font-weight: bold; color: #4ade80; margin-top: 10px; }}
            .log-box {{ background-color: #020617; padding: 15px; border-radius: 8px; font-family: monospace; font-size: 14px; max-height: 250px; overflow-y: auto; border: 1px solid #1e293b; margin-top: 30px; }}
            .status-badge {{ background-color: #22c55e; color: #fff; padding: 6px 12px; border-radius: 20px; font-size: 14px; font-weight: bold; }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>🚀 Venture Foundry Autonomous Command Center</h1>
                <div><span class="status-badge">SYSTEM ONLINE (24/7)</span></div>
            </div>
            
            <div class="card-grid">
                <div class="card">
                    <h3>Tổng Video Đã Xuất Bản</h3>
                    <div class="metric">{total_videos} Shorts</div>
                    <p>Trạng thái vòng lặp PDCA: Đang hoạt động liên tục</p>
                </div>
                <div class="card">
                    <h3>Chu kỳ A/B Testing & Tiến hóa</h3>
                    <div class="metric">{len(history)} Chu kỳ</div>
                    <p>Trạng thái tối ưu hóa: Tự động tinh chỉnh prompt</p>
                </div>
                <div class="card">
                    <h3>Trạng thái Tự Tiến Hóa (Auto-Evolution)</h3>
                    <div class="metric" style="font-size: 24px; color: #38bdf8;">{evolution.get('status', 'Stable')}</div>
                    <p>{evolution.get('adaptation', 'Hệ thống tự động đồng bộ thời gian thực')}</p>
                </div>
            </div>

            <div class="card">
                <h3>🛡️ Nhật ký hoạt động vĩ mô (Live System Log)</h3>
                <div class="log-box" id="log-content">
    """
    
    log_lines = []
    if os.path.exists("output/viral_manager.log"):
        try:
            with open("output/viral_manager.log", "r", encoding="utf-8") as lf:
                log_lines = lf.readlines()[-15:]
        except Exception:
            log_lines = ["Không thể đọc file log."]
            
    for line in log_lines:
        html_content += f"{line.strip()}<br>"
        
    html_content += """
                </div>
            </div>
        </div>
    </body>
    </html>
    """
    return html_content

if __name__ == "__main__":
    import uvicorn
    print("[Dashboard] Khởi động Web Monitoring Dashboard tại http://127.0.0.1:8000")
    uvicorn.run(app, host="127.0.0.1", port=8000)
