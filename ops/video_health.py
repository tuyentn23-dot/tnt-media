# -*- coding: utf-8 -*-
# ops/video_health.py - Kiem tra suc khoe video TRUOC khi dang
# Chan video den, video qua toi, video loi, video qua ngan
import os
import subprocess
import numpy as np
from PIL import Image

FFMPEG = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'tools', 'ffmpeg.exe')
MIN_MEAN = 25.0      # do sang trung binh toi thieu (thap hon = den/qua toi)
MIN_STD = 18.0       # do da dang pixel (thap = 1 mau/den)
MIN_SIZE_BYTES = 300000
MIN_DURATION = 3.0

def _probe(video):
    r = subprocess.run([FFMPEG, '-i', video], capture_output=True, text=True, encoding='utf-8', errors='replace')
    dur = None
    for line in (r.stderr or '').splitlines():
        if 'Duration' in line:
            t = line.split('Duration:')[1].split(',')[0].strip()
            try:
                h, m, s = t.split(':')
                dur = int(h) * 3600 + int(m) * 60 + float(s)
            except Exception:
                pass
    return dur

def _frame_stats(video, frac):
    png = video + '.health.png'
    dur = _probe(video) or 10.0
    t = max(0.5, min(dur - 0.3, dur * frac))
    subprocess.run([FFMPEG, '-y', '-ss', str(t), '-i', video, '-frames:v', '1', png], capture_output=True)
    if not os.path.exists(png):
        return None
    a = np.asarray(Image.open(png).convert('RGB'), dtype='float32')
    try:
        os.remove(png)
    except Exception:
        pass
    return float(a.mean()), float(a.std())

def check(video_path, frames=(0.05, 0.3, 0.5, 0.7, 0.95)):
    """Tra ve dict: ok, reasons, metrics. Chan video den/loi."""
    res = {'ok': True, 'reasons': [], 'metrics': {}}
    if not video_path or not os.path.exists(video_path):
        res['ok'] = False; res['reasons'].append('file-not-found'); return res
    sz = os.path.getsize(video_path)
    res['metrics']['size_bytes'] = sz
    if sz < MIN_SIZE_BYTES:
        res['ok'] = False; res['reasons'].append('file-too-small:' + str(sz))
        return res
    dur = _probe(video_path)
    res['metrics']['duration'] = dur
    if not dur or dur < MIN_DURATION:
        res['ok'] = False; res['reasons'].append('too-short-or-bad'); return res
    stats = []
    for f in frames:
        s = _frame_stats(video_path, f)
        if s is None:
            res['ok'] = False; res['reasons'].append('frame-read-fail:' + str(f)); return res
        stats.append(s)
    means = [x[0] for x in stats]
    stds = [x[1] for x in stats]
    res['metrics']['means'] = [round(m, 1) for m in means]
    res['metrics']['stds'] = [round(s, 1) for s in stds]
    res['metrics']['mean_avg'] = round(sum(means) / len(means), 1)
    res['metrics']['std_avg'] = round(sum(stds) / len(stds), 1)
    # Video den: da so frame toi va it da dang
    dark = sum(1 for m, s in stats if m < 12 and s < 25)
    res['metrics']['dark_frames'] = dark
    if dark >= 3:
        res['ok'] = False; res['reasons'].append('mostly-black:' + str(dark) + '/' + str(len(stats)))
    elif res['metrics']['mean_avg'] < MIN_MEAN and res['metrics']['std_avg'] < MIN_STD:
        res['ok'] = False; res['reasons'].append('too-dark-and-flat')
    # Video 1 mau (ColorClip) - std cuc thap o moi frame
    flat = sum(1 for m, s in stats if s < 10)
    if flat >= 4:
        res['ok'] = False; res['reasons'].append('flat-color:' + str(flat))
    return res

if __name__ == '__main__':
    import sys, json
    print(json.dumps(check(sys.argv[1]), ensure_ascii=False, indent=2))
