# Topic A/B Matrix - TNT Media P1 Module
# Global winners x durations x hook styles. Persists experiment state, picks next variant.
# Research 2026-09-10: 13-20s sweet spot; hook=peak frame; no voice for top topics.
import os
import json
import logging
import random
import argparse
from datetime import datetime

logging.basicConfig(filename="output/viral_manager.log", level=logging.INFO)
log = logging.getLogger("abmatrix")

TOPICS = ["satisfying", "food", "magic", "cat", "dog"]
DURATIONS = [13, 15, 18, 20]
HOOKS = ["peak", "cold"]
STATE = "memory/ab_matrix_state.json"


def all_variants():
    out = []
    for t in TOPICS:
        for d in DURATIONS:
            for h in HOOKS:
                out.append({"topic": t, "duration": d, "hook": h})
    return out


def load_state():
    if os.path.exists(STATE):
        return json.load(open(STATE))
    return {"results": {}, "updated": None}


def save_state(s):
    os.makedirs("memory", exist_ok=True)
    s["updated"] = datetime.utcnow().isoformat()
    json.dump(s, open(STATE, "w"), indent=2)


def key(v):
    return v["topic"] + "" + str(v["duration"]) + "" + v["hook"]


def record(topic, duration, hook, views, retention=None):
    s = load_state()
    k = topic + "" + str(duration) + "" + hook
    r = s["results"].get(k, {"topic": topic, "duration": duration, "hook": hook, "runs": 0, "views": 0})
    r["runs"] += 1
    r["views"] += views
    r["avg_views"] = round(r["views"] / r["runs"], 2)
    if retention is not None:
        r["retention"] = retention
    s["results"][k] = r
    save_state(s)
    return r


def pick_next(explore=0.3):
    s = load_state()
    variants = all_variants()
    untried = [v for v in variants if key(v) not in s["results"]]
    if untried and random.random() < (1 - explore):
        return random.choice(untried)
    done = [v for v in variants if key(v) in s["results"]]
    if not done:
        return random.choice(variants)
    done.sort(key=lambda v: s["results"][key(v)].get("avg_views", 0), reverse=True)
    return done[0]


def best(n=5):
    s = load_state()
    vals = list(s["results"].values())
    vals.sort(key=lambda r: r.get("avg_views", 0), reverse=True)
    return vals[:n]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--pick", action="store_true")
    ap.add_argument("--best", action="store_true")
    args = ap.parse_args()
    if args.best:
        print(json.dumps(best(), indent=2))
    else:
        print(json.dumps(pick_next(), indent=2))


if __name__ == "__main__":
    main()
