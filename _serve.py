import os
PORT = int(os.environ.get("PORT", os.environ.get("DASH_PORT", "8787")))
HOST = os.environ.get("HOST", "0.0.0.0")
os.environ["DASH_PORT"] = str(PORT)
import sys
sys.path.insert(0, '.')
from ops import control_center as C
try:
 C.start_worker()
except Exception:
 pass
try:
 import json, io
 c = json.load(io.open("memory/autopilot.json", encoding="utf-8"))
 if c.get("enabled"):
  from ops import autopilot as ap
  ap.start()
except Exception:
 pass
import uvicorn
uvicorn.run(C.app, host=HOST, port=PORT, log_level="warning")
