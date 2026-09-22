# -- coding: utf-8 --
"""decision_to_publish - noi decision B vao auto_publish that (YC1). Dry-run mac dinh."""
import sqlite3, os, sys, json
ROOT = os.getcwd()
sys.path.insert(0, ROOT)
DB = os.path.join(ROOT, 'system', 'state.db')
FOOTAGE = {'animal': ['animal', 'animals', 'cute_animals'], 'anime': ['anime'], 'body': ['body'], 'food': ['food'], 'space': ['space', 'pexspace'], 'ocean': ['ocean'], 'psychology': ['psychology'], 'roblox': ['roblox'], 'science': ['science'], 'gacha': ['gacha'], 'nostalgia': ['nostalgia'], 'nature': ['nature']}
def usable():
    d = os.path.join(ROOT, 'library')
    out = []
    for name in os.listdir(d):
        p = os.path.join(d, name)
        if os.path.isdir(p) and any(x.endswith('.mp4') for x in os.listdir(p)):
            out.append(name)
    return out
def pick_footage(topic, avail):
    t = (topic or '').lower()
    for key, folders in FOOTAGE.items():
        if key in t:
            for fol in folders:
                if fol in avail:
                    return fol
    for fol in avail:
        if fol in t:
            return fol
    return avail[0] if avail else None
def choose(limit=3):
    con = sqlite3.connect(DB)
    con.row_factory = sqlite3.Row
    avail = usable()
    sel = 'SELECT id, channelId, topic, format, hook FROM decisions ORDER BY score DESC, id DESC LIMIT ?'
    rows = con.execute(sel, (limit,)).fetchall()
    con.close()
    plan = []
    for r in rows:
        d = dict(decisionId=r['id'], channelId=r['channelId'], topic=r['topic'], format=r['format'])
        d['footage'] = pick_footage(r['topic'], avail)
        plan.append(d)
    return plan
def main():
    dry = ('--publish' not in sys.argv)
    plan = choose(3)
    print('plan:', json.dumps(plan, ensure_ascii=False, indent=2).encode('ascii','replace').decode())
    if dry:
        print('DRY-RUN (them --publish de dang that)')
        return
    from ops.auto_publish import run
    for p in plan:
        topic = p['footage']
        if not topic:
            continue
        r = run(topic=topic, target_dur=14.0)
        print('published', str(topic), r.get('ok'), r.get('youtube_id'))
if __name__ == '__main__':
    main()
