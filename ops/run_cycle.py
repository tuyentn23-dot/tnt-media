# Full Production Cycle - TNT Media
# footage -> retention optimize -> (optionally) publish. Testable end-to-end.
import os
import json
import logging
import argparse
from datetime import datetime

logging.basicConfig(filename="output/viral_manager.log", level=logging.INFO)
log = logging.getLogger("cycle")


def pick_topic():
    try:
        from ops.daily_topic_decider import decide
        plan = decide(1)
        posts = plan.get("posts", [])
        return posts[0] if posts else {"topic": "satisfying", "duration": 15, "hook": "peak"}
    except Exception as e:
        log.warning("pick topic failed: " + str(e))
        return {"topic": "satisfying", "duration": 15, "hook": "peak"}


def get_clip(topic):
    from ops.real_footage_pipeline import best_clips
    clips = best_clips(topic, 1)
    return clips[0] if clips else None


def run_cycle(topic=None, publish=False):
    result = {"started": datetime.now().isoformat()}
    plan = pick_topic() if topic is None else {"topic": topic, "duration": 15}
    topic = plan["topic"]
    dur = int(plan.get("duration", 15))
    result["topic"] = topic
    result["duration"] = dur
    src = get_clip(topic)
    result["source_clip"] = src
    if not src:
        result["status"] = "no_footage"
        return result
    from ops.viral_optimizer import optimize_viral, gate
    out = "output/cycle_" + topic + "_" + datetime.now().strftime("%H%M%S") + ".mp4"
    music = "library/music_bed.wav" if os.path.exists("library/music_bed.wav") else None
    final = optimize_viral(src, output_path=out, target=dur, music_path=music)
    g = gate(final)
    result["viral_score"] = g.get("viral_score")
    result["passes_gate"] = g.get("passes_gate")
    result["status"] = "optimized"
    if publish:
        try:
            from ops.platform_publisher import unified_publish
            pid = unified_publish(final, title="TNT Short " + topic)
            result["published"] = str(pid)
            result["status"] = "published"
            try:
             from ops.topic_ab_matrix import record
             record(topic, dur, "peak", 0)
            except Exception:
             pass
        except Exception as e:
            result["publish_error"] = str(e)
    result["finished"] = datetime.now().isoformat()
    json.dump(result, open("memory/last_cycle.json", "w"), indent=2)
    log.info("cycle done: " + json.dumps(result))
    return result


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--topic", default=None)
    ap.add_argument("--publish", action="store_true")
    args = ap.parse_args()
    print(json.dumps(run_cycle(args.topic, args.publish), indent=2))


if __name__ == "__main__":
    main()
