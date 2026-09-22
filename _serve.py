import os
os.environ["DASH_PORT"]="8787"
import sys
sys.path.insert(0,".")
from ops import control_center as C
try:
	C.start_worker()
except Exception:
	pass
# autostart autopilot if enabled in config
try:
	import json, io
	c=json.load(io.open("memory/autopilot.json",encoding="utf-8"))
	if c.get("enabled"):
		from ops import autopilot as ap
		ap.start()
except Exception:
	pass
import uvicorn
uvicorn.run(C.app, host="127.0.0.1", port=8787, log_level="warning")