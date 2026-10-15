"""Compatibility entry point for the TNT scene analyzer.

Supports both: python ops/video_analyzer.py VIDEO [--output DIR]
and: from ops.video_analyzer import analyze_video
"""
import argparse
import json
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from ops.scene_reader import analyze_video as _analyze_video
from ops.video_reader import read_video


def analyze_video(path, output=None, **kwargs):
    output = output or ROOT / 'reports' / ('analysis_' + Path(path).stem)
    return _analyze_video(path, output, **kwargs)


analyze = analyze_video


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('video')
    parser.add_argument('--output')
    parser.add_argument('--vision', action='store_true')
    parser.add_argument('--vision-timeout', type=int, default=30)
    parser.add_argument('--threshold', type=float, default=0.28)
    parser.add_argument('--max-scenes', type=int, default=120)
    args = parser.parse_args()
    if not 1 <= args.vision_timeout <= 300:
        parser.error('vision-timeout must be 1..300 seconds')
    output = Path(args.output) if args.output else ROOT / 'reports' / ('analysis_' + Path(args.video).stem)
    try:
        result = analyze_video(args.video, output, use_vision=args.vision,
                               vision_timeout=args.vision_timeout,
                               threshold=args.threshold, max_scenes=args.max_scenes)
    except (OSError, ValueError, RuntimeError, subprocess.TimeoutExpired) as exc:
        parser.exit(1, f'Analysis failed: {exc}\n')
    print(json.dumps({'ok': True, 'scenes': len(result['scenes']),
                      'vision_completed': result['vision_completed'],
                      'report': str(output.resolve() / 'index.html')}))


if __name__ == '__main__':
    main()
