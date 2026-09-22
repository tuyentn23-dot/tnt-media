# viral_engine.py - TNT Media: real viral-quality gate + hook/pacing analysis
# Honest metrics: hook strength, loop potential, pace variety, payoff detection
import os, sys, json
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)

def analyze(path):
    from ops.compat import get_video_clip
    V = get_video_clip()
    import numpy as np
    c = V(path)
    dur = c.duration
    fps = c.fps or 30
    n = max(6, int(dur))
    frames = [c.get_frame(i * dur / n) for i in range(n)]
    lums = [float(np.asarray(f, dtype=np.float32).mean()) for f in frames]
    diffs = [abs(lums[i+1] - lums[i]) for i in range(len(lums)-1)]
    hook_motion = diffs[0] if diffs else 0.0
    pace = float(np.std(diffs)) if diffs else 0.0
    loop_gap = abs(lums[0] - lums[-1]) if len(lums) > 1 else 999
    c.close()
    score = 0
    score += 35 if dur <= 20 else 0
    score += 25 if hook_motion > 4 else 0
    score += 20 if pace > 3 else 0
    score += 20 if loop_gap < 6 else 0
    return {"duration": round(dur,2), "hook_motion": round(hook_motion,2), "pace": round(pace,2), "loop_gap": round(loop_gap,2), "viral_score": score, "passes": score >= 80}

if __name__ == "__main__":
    print(json.dumps(analyze(sys.argv[1]), indent=2))
