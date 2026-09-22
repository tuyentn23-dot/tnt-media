# -- coding: utf-8 --
import sqlite3, os, json
from datetime import datetime
ROOT = os.getcwd()
A = os.path.join(ROOT, 'memory', 'tnt_media.db')
B = os.path.join(ROOT, 'system', 'state.db')
now = lambda: datetime.now().isoformat(timespec='seconds')
ca = sqlite3.connect(A)
ca.row_factory = sqlite3.Row
cb = sqlite3.connect(B)
cb.row_factory = sqlite3.Row
ch = {r['name']: r['id'] for r in cb.execute('SELECT id, name FROM channels')}
def channel_id(topic):
    t = topic or ''
    for name in sorted(ch, key=len, reverse=True):
        if t.startswith('ch' + name) or t.startswith(name):
            return ch[name]
    return 1
for t in ['publishes', 'analytics', 'videos']:
    cb.execute('DELETE FROM ' + t)
vids = ca.execute('SELECT id, cycle_id, path, youtube_id, title, topic, format, score, status, published_at, created_at FROM videos').fetchall()
nv = 0
for v in vids:
    cb.execute('INSERT INTO videos (id, channelId, decisionId, path, status, renderWorker, renderMs, metaJson, createdAt) VALUES (?,?,?,?,?,?,?,?,?)', (v['id'], channel_id(v['topic']), v['cycle_id'], v['path'] or 'unknown.mp4', v['status'] or 'unknown', 'nhanh_a', None, json.dumps({'topic': v['topic'], 'title': v['title'], 'format': v['format'], 'score': v['score'], 'youtube_id': v['youtube_id'], 'published_at': v['published_at']}, ensure_ascii=False), v['created_at'] or now()))
    nv += 1
np = 0
for v in vids:
    if not v['youtube_id']:
        continue
    cb.execute('INSERT INTO publishes (videoId, platform, url, publishedAt, status, errorText, metaJson) VALUES (?,?,?,?,?,?,?)', (v['id'], 'youtube', 'https://www.youtube.com/watch?v=' + v['youtube_id'], v['published_at'] or now(), 'ok', None, json.dumps({'topic': v['topic'], 'title': v['title']}, ensure_ascii=False)))
    np += 1
nm = 0
for m in ca.execute('SELECT video_id, ts, views, ctr, retention, likes, comments FROM metrics').fetchall():
    cb.execute('INSERT INTO analytics (videoId, views, likes, comments, retention, ctr, fetchedAt) VALUES (?,?,?,?,?,?,?)', (m['video_id'], m['views'], m['likes'], m['comments'], m['retention'], m['ctr'], m['ts'] or now()))
    nm += 1
cb.commit()
cb.execute('INSERT INTO changelog (version, entity, change, actor, createdAt) VALUES (?,?,?,?,?)', ('A->B', 'sync', 'videos=%d publishes=%d analytics=%d' % (nv, np, nm), 'sync_a_to_b', now()))
cb.commit()
print('A->B done: videos=%d publishes=%d analytics=%d' % (nv, np, nm))
ca.close()
cb.close()
