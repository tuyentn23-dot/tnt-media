import json, os
from datetime import datetime
try:
    with open("ROADMAP.md", "r", encoding="utf-8") as f:
        r = f.read()
    r = r.replace("- [ ] Bước 1.1: Setup môi trường và cài đặt CrewAI, Perplexity API.", "- [x] Bước 1.1: Setup môi trường và cài đặt CrewAI, Perplexity API.")
    with open("ROADMAP.md", "w", encoding="utf-8") as f:
        f.write(r)
    
    with open("memory/upgrade_state.json", "r", encoding="utf-8") as f:
        s = json.load(f)
    s["current_step"] = "1.2"
    s["blockers"] = "Cần code Agent 1 (Researcher) tìm Trend"
    s["last_successful_run"] = datetime.now().isoformat() + "Z"
    with open("memory/upgrade_state.json", "w", encoding="utf-8") as f:
        json.dump(s, f, indent=2, ensure_ascii=False)
    print("Trang thai he thong da duoc cap nhat!")
except Exception as e:
    print("Error:", e)
