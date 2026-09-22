"""TNT Media OS - PDCA orchestrator."""
from .. import db
from .. import models as M
from . import plan as PLAN, do as DO, check as CHECK, act as ACT

def run_once(goal=None):
    cid = M.create_cycle(goal=goal or "PDCA run", stage="plan")
    log = {"cycle_id": cid}
    p = PLAN.propose(goal)
    log["plan"] = p
    M.update_cycle(cid, stage="do")
    d = DO.execute(cid, p)
    log["do"] = d
    M.update_cycle(cid, stage="check")
    c = CHECK.run(cid, limit=10)
    log["check"] = c
    M.update_cycle(cid, stage="act")
    a = ACT.run(cid)
    log["act"] = a
    M.update_cycle(cid, stage="done", status="completed", ended_at=db.now())
    return log

