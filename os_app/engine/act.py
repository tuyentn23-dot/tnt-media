"""TNT Media OS - ACT stage."""
from .. import models as M

def run(cycle_id):
    insights = M.list_insights(30)
    decisions = []
    top_n = len([i for i in insights if i["kind"] == "top_performer"])
    if top_n > 0:
        d = M.Decision(cycle_id=cycle_id, rule_key="topic_weight", old_value="uniform", new_value="boost_winners", reason="Found " + str(top_n) + " top performers", result={"top_n": top_n})
        M.add_decision(d)
        decisions.append("topic_weight=boost_winners")
    low_q = [i for i in insights if i["kind"] == "quality_audit" and "passes" in i.get("evidence", {}) and not i["evidence"].get("passes")]
    if len(low_q) >= 1 and no_open_exp():
        eid = M.add_experiment(M.Experiment(name="auto_hook_ab" + str(cycle_id), variant_a="current", variant_b="stronger_hook", metric="hook_motion"))
        d = M.Decision(cycle_id=cycle_id, rule_key="quality_gate", old_value="publish_any", new_value="experiment_hook", reason="low quality count=" + str(len(low_q)), result={"experiment_id": eid})
        M.add_decision(d)
        decisions.append("quality_gate=experiment_hook(" + str(eid) + ")")
    return {"cycle_id": cycle_id, "decisions": decisions}

def _no_open_exp():
    try:
        exps = M.list_experiments(20)
        return not any(e.get("winner") is None for e in exps)
    except Exception:
        return True
