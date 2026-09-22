"""TNT Media OS - PLAN stage."""
from .. import models as M

def propose(goal=None):
    cycles = M.list_cycles(20)
    videos = M.list_videos(50)
    insights = M.list_insights(10)
    plan = {
        "goal": goal or "Auto: continue improving retention & CTR",
        "prior_cycles": len(cycles),
        "known_videos": len(videos),
        "recent_insights": [i["finding"] for i in insights[:5]],
        "suggested_topic": "science_loop",
        "suggested_format": "shorts_60s",
    }
    return plan

