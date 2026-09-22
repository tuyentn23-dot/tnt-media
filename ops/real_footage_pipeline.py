# Real Footage Pipeline - TNT Media P0 Module
# Global research 2026-09-10: real footage beats synthetic; winners = satisfying/food/magic/cat/dog
# Downloads bulk real clips by topic, scores by motion/contrast, stores in library/<topic>/
import os
import json
import logging
import argparse
import urllib.request
import hashlib
from datetime import datetime

logging.basicConfig(filename="output/viral_manager.log", level=logging.INFO)
log = logging.getLogger("footage")

# Ensure bundled ffmpeg is visible to moviepy in ALL entry paths (CLI + imports)
import os as _os
_ff = _os.path.join(_os.path.dirname(_os.path.dirname(_os.path.abspath(__file__))), "tools", "ffmpeg.exe")
if _os.path.exists(_ff) and not _os.environ.get("IMAGEIO_FFMPEG_EXE"):
 _os.environ["IMAGEIO_FFMPEG_EXE"] = _ff


LIBRARY = "library"
SOURCES = "analytics/real_footage_sources.json"
MIN_CLIP_SECONDS = 2
MAX_BYTES = 80 * 1024 * 1024 # raised from 12MB: mixkit 1080p clips are 30-95MB


def load_sources():
    if not os.path.exists(SOURCES):
        return {}
    with open(SOURCES, "r", encoding="utf-8") as f:
        return json.load(f)


def url_to_name(url):
    h = hashlib.md5(url.encode("utf-8")).hexdigest()[:10]
    return h + ".mp4"


def resolve_variants(url):
    if url.endswith("_large.mp4"):
     base = url[:-10]
     return [base + "_medium.mp4", base + "_small.mp4", url]
    return [url]


def download(url, dest, timeout=25):
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=timeout) as r:
            data = r.read(MAX_BYTES + 1)
            if len(data) > MAX_BYTES:
             log.info("skip oversized " + url)
             return False
            with open(dest, "wb") as out:
             out.write(data)
        return True
    except Exception as e:
        log.warning("download failed " + url + " : " + str(e))
        return False


def score_clip(path):
    try:
        from ops.compat import get_video_clip; VideoFileClip = get_video_clip()
        import numpy as np
        c = VideoFileClip(path)
        if c.duration < MIN_CLIP_SECONDS:
            return 0.0
        samples = 10
        vals = []
        for i in range(samples):
            t = c.duration * (i + 1) / (samples + 1)
            fr = c.get_frame(t)
            lum = np.asarray(fr, dtype=np.float32).mean(axis=2)
            vals.append(float(lum.std() / 128.0))
        return round(float(np.mean(vals)), 4)
    except Exception as e:
        log.warning("score failed " + path + " : " + str(e))
        return 0.0


def fetch_topic(topic, urls, limit=8):
    topic_dir = os.path.join(LIBRARY, topic)
    os.makedirs(topic_dir, exist_ok=True)
    manifest_path = os.path.join(topic_dir, "_manifest.json")
    manifest = json.load(open(manifest_path)) if os.path.exists(manifest_path) else []
    have = set(m["file"] for m in manifest)
    count = 0
    for url in urls:
        name = url_to_name(url)
        if name in have:
            continue
        dest = os.path.join(topic_dir, name)
        ok = False
        used = url
        for v in resolve_variants(url):
            if download(v, dest):
             ok = True
             used = v
             break
        if not ok:
            continue
        score = score_clip(dest)
        manifest.append({"file": name, "url": used, "score": score, "topic": topic})
        log.info("footage " + topic + " " + name + " score=" + str(score))
        count += 1
        if count >= limit:
            break
    manifest.sort(key=lambda m: m["score"], reverse=True)
    with open(manifest_path, "w", encoding="utf-8") as f:
        json.dump(manifest, f, indent=2)
    return count, len(manifest)


def best_clips(topic, n=3):
    manifest_path = os.path.join(LIBRARY, topic, "_manifest.json")
    if not os.path.exists(manifest_path):
        return []
    manifest = json.load(open(manifest_path))
    return [os.path.join(LIBRARY, topic, m["file"]) for m in manifest[:n]]


def run(topics=None, limit=8):
    src = load_sources()
    if topics is None:
        topics = list(src.keys())
    report = {}
    for topic in topics:
        urls = src.get(topic, [])
        if not urls:
            log.info("no urls for topic " + topic)
            continue
        new, total = fetch_topic(topic, urls, limit)
        report[topic] = {"new": new, "total": total}
    with open(os.path.join(LIBRARY, "_pipeline_report.json"), "w", encoding="utf-8") as f:
        json.dump(report, f, indent=2)
    return report


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--topics", default=None)
    ap.add_argument("--limit", type=int, default=8)
    args = ap.parse_args()
    topics = args.topics.split(",") if args.topics else None
    rep = run(topics, args.limit)
    print(json.dumps(rep, indent=2))


if __name__ == "__main__":
    main()
