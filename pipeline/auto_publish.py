# pipeline/auto_publish.py - Auto-publish scheduled publications
import os, sys
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)
from pipeline import state


def publish_due():
    """Dang cac publication den gio. Tra ve so luong da dang."""
    try:
        c = state.connect()
    except Exception:
        return 0
    now_key = state.now().replace('T', ' ')[:16]
    try:
        rows = c.execute(
            "SELECT id, channel_id, file_path, title FROM publications "
            "WHERE status='scheduled' AND schedule_at IS NOT NULL "
            "AND substr(schedule_at,1,16) <= ?",
            (now_key,),
        ).fetchall()
    except Exception:
        rows = []
    c.close()
    done = 0
    for r in rows:
        try:
            from ops import os_publish as _op
            ttl = r['title'] or ('Video ' + str(r['id']))
            res = _op.publish(r['file_path'], ttl, '', force=False)
            vid = None
            if isinstance(res, dict):
                vid = res.get('youtube_id') or res.get('id') or res.get('video_id')
        except Exception as e:
            print('[auto_publish] fail ' + str(r['id']) + ': ' + str(e)[:150], flush=True)
            vid = None
        cc = state.connect()
        try:
            if vid:
                cc.execute(
                    'UPDATE publications SET status=?, youtube_id=?, published_at=?, schedule_at=NULL WHERE id=?',
                    ('published', vid, state.now(), r['id']),
                )
                done += 1
            else:
                cc.execute(
                    'UPDATE publications SET status=? WHERE id=?',
                    ('publish_failed', r['id']),
                )
            cc.commit()
        except Exception:
            pass
        finally:
            cc.close()
    return done
