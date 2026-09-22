# -- coding: utf-8 --
"""TNT Media OS - auto publish v3: fresh topic, fresh file, no republish, Vietnamese script."""
import os, sys, glob, time
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)
os.environ.setdefault('IMAGEIO_FFMPEG_EXE', os.path.join(ROOT, 'tools', 'ffmpeg.exe'))

MUSIC_MAP = dict([
    ('cat', 'music_cat.wav'),
    ('dog', 'music_dog.wav'),
    ('food', 'music_food.wav'),
    ('magic', 'music_magic.wav'),
    ('satisfying', 'music_satisfying.wav'),
    ('satisfy2', 'music_satisfying.wav'),
])

def _music_for(topic, music_path=None):
    if music_path and os.path.exists(music_path):
        return music_path
    name = MUSIC_MAP.get((topic or '').lower())
    if name:
        p = os.path.join(ROOT, 'library', name)
        if os.path.exists(p):
            return p
    try:
        import hashlib, glob
        bank = sorted(glob.glob(os.path.join(ROOT, 'music_bank', '*.wav')))
        if bank:
            h = int(hashlib.sha1((topic or '').encode('utf-8')).hexdigest(), 16)
            return bank[h % len(bank)]
    except Exception:
        pass
    bed = os.path.join(ROOT, 'library', 'music_bed.wav')
    return bed if os.path.exists(bed) else None

def _pool(topic):
    d = os.path.join(ROOT, 'library', topic)
    if not os.path.isdir(d):
        return []
    return sorted(glob.glob(os.path.join(d, '*.mp4')))

def _already_published(topic):
    try:
        from os_app import db
        c = db.connect()
        row = c.execute('SELECT COUNT(1) FROM videos WHERE lower(topic)=? AND youtube_id IS NOT NULL', ((topic or '').lower(),)).fetchone()
        return (row and row[0]) > 0
    except Exception:
        return False

def run(topic=None, target_dur=14.0, force=False, privacy='public', title=None, description='', tags=None, cycle_id=None, voice_name=None, allow_republish=False):
    from ops.video_build import build_short
    from ops.video_quality import rank_footage
    from ops.quality_gate import evaluate
    if not topic:
        from ops import topic_picker as _tp
        topic = _tp.pick()
    if not topic:
        return dict(ok=False, error='no fresh topic')
    if not allow_republish and _already_published(topic):
        return dict(ok=False, error='already published: ' + topic, topic=topic)
    hook_text = None
    script_lines = []
    try:
        from ops import content_planner as _cp
        hook_text, script_lines, _hint = _cp.for_topic(topic)
    except Exception:
        pass
    pool = _pool(topic)
    if not pool:
        return dict(ok=False, error='no footage: ' + topic, topic=topic)
    best = rank_footage(pool)[:4]
    ts = time.strftime('%Y%m%d_%H%M%S')
    fname = 'short' + chr(95) + str(topic) + chr(95) + ts + '.mp4'
    out = os.path.join(ROOT, 'output', fname)
    vt = ' '.join(str(x) for x in script_lines) if script_lines else None
    mus = _music_for(topic)
    build_short(best, script_lines, out, hook_text=hook_text, music_path=mus, target_dur=float(target_dur), voice_text=vt, voice_name=voice_name)
    if not vt or len(str(vt).strip()) < 10:
        return dict(ok=False, blocked=True, error='no voiceover text (quality rule)', topic=topic)
    gate = evaluate(out)
    if not gate.get('passes'):
        return dict(ok=False, blocked=True, video=out, quality=gate, topic=topic)
    if not title:
        title = (hook_text or topic) + ' #shorts'
    if not description and script_lines:
        description = (' | ').join([str(x) for x in script_lines[:2]]) + ' #shorts #viral #tiktok'
    if not tags:
        tags = [topic, 'shorts', 'viral', 'tiktok']
    from ops.os_publish import publish
    res = publish(out, title, description=description, tags=tags, privacy=privacy, topic=topic, cycle_id=cycle_id, force=True)
    res['quality'] = gate
    res['topic'] = topic
    res['video'] = out
    return res