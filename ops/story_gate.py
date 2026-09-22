# story_gate.py - quality gate for story/what-if videos (content-based)
import os, sys, json
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)

def gate(path, item=None):
    from ops.compat import get_video_clip
    V = get_video_clip()
    c = V(path)
    score = 0
    dur = c.duration
    score += 30 if 15 <= dur <= 60 else 0
    score += 30 if c.audio is not None else 0
    score += 20 if c.w < c.h else 0
    score += 20 if (item and item.get("hook")) else 0
    info = {"duration": round(dur,1), "has_audio": c.audio is not None, "vertical": c.w<c.h, "has_hook": bool(item and item.get("hook")), "story_score": score}
    c.close()
    info["passes"] = score >= 80
    return info

if __name__ == "__main__":
    print(json.dumps(gate(sys.argv[1]), indent=2))
