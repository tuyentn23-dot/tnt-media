# Daily Topic Decider - TNT Media P1 Module
# Reads A/B matrix results + retention log, picks the next best topic/duration/hook.
# Writes memory/daily_plan.json for the publisher to consume.
import os
import json
import logging
from datetime import datetime

logging.basicConfig(filename="output/viral_manager.log", level=logging.INFO)
log = logging.getLogger("daily")

PLAN = "memory/daily_plan.json"
AB = "memory/ab_matrix_state.json"
RET = "memory/retention_log.json"


def read_json(path, default):
    if os.path.exists(path):
        try:
            return json.load(open(path))
        except Exception:
            return default
    return default


def decide(posts_per_day=3):
    ab = read_json(AB, {"results": {}})
    ret = read_json(RET, [])
    results = list(ab.get("results", {}).values())
    results.sort(key=lambda r: r.get("avg_views", 0), reverse=True)
    plan = {"created": datetime.now().isoformat(), "posts": [], "source": "ab_matrix"}
    for r in results[:posts_per_day]:
        plan["posts"].append({"topic": r["topic"], "duration": r["duration"], "hook": r["hook"], "expected_avg_views": r.get("avg_views", 0)})
    if not plan["posts"]:
        plan["posts"] = [
            {"topic": "satisfying", "duration": 15, "hook": "peak"},
            {"topic": "food", "duration": 15, "hook": "peak"},
            {"topic": "magic", "duration": 15, "hook": "peak"},
        ]
        plan["source"] = "global_winners_default"
    plan["retention_entries"] = len(ret)
    os.makedirs("memory", exist_ok=True)
    json.dump(plan, open(PLAN, "w"), indent=2)
    log.info("daily plan written")
    return plan


def main():
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument("--posts", type=int, default=3)
    args = ap.parse_args()
    print(json.dumps(decide(args.posts), indent=2))


if __name__ == "__main__":
    main()
