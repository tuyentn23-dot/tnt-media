"""TNT Media OS - DO stage (run tools)."""
from .. import models as M
from ..adapters import tool_adapter as TA

DEFAULT_RENDER_TOOLS = [] # add tool names to enable rendering

def execute(cycle_id, plan):
    log = []
    for tool in DEFAULT_RENDER_TOOLS:
        r = TA.run_tool(tool, [], cycle_id=cycle_id, timeout=1800)
        log.append({"tool": tool, "result": r})
    return {"cycle_id": cycle_id, "actions": log}

