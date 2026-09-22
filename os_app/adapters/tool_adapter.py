"""TNT Media OS - adapter to run ops tools and log results."""
import json
import os
import subprocess
import sys
import time
from pathlib import Path
from .. import db
from .. import models as M

HERE = Path(os.getcwd())
OPS = HERE / "ops"
REG = HERE / "memory" / "tool_registry.json"

def load_registry():
    if not REG.exists():
        return {"total": 0, "tools": []}
    return json.loads(REG.read_text(encoding="utf-8"))

def list_tools(cat=None):
    tools = load_registry().get("tools", [])
    if cat:
        tools = [t for t in tools if t.get("cat") == cat]
    return tools

def run_tool(name, args=None, cycle_id=None, timeout=600):
    args = args or []
    script = OPS / name
    if not script.exists():
        return {"ok": False, "error": "tool not found: " + name}
    env = dict(os.environ)
    env["PYTHONPATH"] = str(HERE)
    t0 = time.time()
    try:
        r = subprocess.run([sys.executable, str(script)] + args, cwd=str(HERE), env=env, capture_output=True, text=True, timeout=timeout)
        ms = int((time.time() - t0) * 1000)
        ok = (r.returncode == 0)
        out = (r.stdout or "") + (r.stderr or "")
    except Exception as e:
        ok = False
        out = str(e)
        ms = int((time.time() - t0) * 1000)
    M.log_tool_run(cycle_id, name, {"args": args}, ok, ms, out)
    return {"ok": ok, "ms": ms, "output": out[-4000:]}

