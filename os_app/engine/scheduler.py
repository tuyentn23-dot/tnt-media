"""TNT Media OS - simple scheduler (background thread, PID file)."""
import os
import threading
import time
from pathlib import Path
from . import orchestrator as ORCH

STATE = {"running": False, "last_run": None, "interval_sec": 3600, "thread": None}

def _loop():
    while STATE["running"]:
        try:
            log = ORCH.run_once(goal="scheduled PDCA")
            STATE["last_run"] = log.get("cycle_id")
        except Exception as e:
            print("[scheduler] cycle error:", e)
        for _ in range(STATE["interval_sec"]):
            if not STATE["running"]:
                break
            time.sleep(1)

def start(interval_sec=3600):
    if STATE["running"]:
        return {"already_running": True}
    STATE["interval_sec"] = int(interval_sec)
    STATE["running"] = True
    t = threading.Thread(target=_loop, daemon=True)
    STATE["thread"] = t
    t.start()
    return {"started": True, "interval_sec": STATE["interval_sec"]}

def stop():
    STATE["running"] = False
    return {"stopped": True}

def status():
    return {"running": STATE["running"], "last_run": STATE["last_run"], "interval_sec": STATE["interval_sec"]}

