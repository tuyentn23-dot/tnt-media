# captions.py - burn big centered captions onto video (retention booster)
import os
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def wrap(text, width=22):
    words = text.split()
    lines = []
    cur = ""
    for w in words:
        if len(cur) + len(w) + 1 <= width:
            cur = (cur + " " + w).strip()
        else:
            lines.append(cur)
            cur = w
    if cur: lines.append(cur)
    return chr(10).join(lines)

def caption_clips(story):
    return [wrap(story["hook"]), wrap(story["body"]), wrap(story["payoff"])]
