# -- coding: utf-8 --
import sqlite3, os, json, urllib.request, urllib.parse
from datetime import datetime
ROOT = os.getcwd()
DB = os.path.join(ROOT, 'system', 'state.db')
SEEDS = ['meo', 'cho', 'anime', 'roblox', 'gacha', 'lifehack', 'bi an', 'khoa hoc', 'vu tru', 'am nhac']
now = lambda: datetime.now().isoformat(timespec='seconds')

def suggest(q, hl='vi'):
    u = 'https://suggestqueries.google.com/complete/search?client=firefox&hl=' + hl + '&q=' + urllib.parse.quote(q)
    try:
        r = urllib.request.urlopen(u, timeout=10).read().decode('utf-8', errors='replace')
        data = json.loads(r)
        return [s for s in data[1] if isinstance(s, str)]
    except Exception:
        return []

def score_of(rank, total):
    if total <= 1:
        return 1.0
    return round(1.0 - (rank / float(total)), 3)

def main():
    con = sqlite3.connect(DB)
    seen = set()
    rows = []
    ts = now()
    for seed in SEEDS:
        sugs = suggest(seed)
        total = len(sugs)
        for i, topic in enumerate(sugs):
            key = topic.strip().lower()
            if not key or key in seen:
                continue
            seen.add(key)
            rows.append(('google_suggest', 'VN', topic.strip(), score_of(i, total), None, None, ts, json.dumps({'seed': seed, 'rank': i}, ensure_ascii=False)))
    con.executemany('INSERT INTO trends (source, region, topic, score, volume, growth, snapshotAt, metaJson) VALUES (?,?,?,?,?,?,?,?)', rows)
    con.execute('INSERT INTO changelog (version, entity, change, actor, createdAt) VALUES (?,?,?,?,?)', ('trend_scan', 'trends', 'fetched=%d' % len(rows), 'trend_scan', ts))
    con.commit()
    print('trend_scan done: trends=%d' % len(rows))
    con.close()

if __name__ == '__main__':
    main()
