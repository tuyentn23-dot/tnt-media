# -- coding: utf-8 --
"""TNT Media OS - autopublish runner. Picks fresh viral topic, builds, publishes."""
import os, sys, time, json
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)
LOG = os.path.join(ROOT, 'logs', 'autopublish.log')
COOLDOWN = int(os.environ.get('TNT_PUB_COOLDOWN', '10800'))
STATE = os.path.join(ROOT, 'memory', 'autopublish_state.json')


def _log(msg):
    try:
        os.makedirs(os.path.dirname(LOG), exist_ok=True)
        with open(LOG, 'a', encoding='utf-8') as f:
            f.write(time.strftime('%Y-%m-%d %H:%M:%S ') + str(msg) + chr(10))
    except Exception:
        pass


def _last_ts():
    try:
        d = json.load(open(STATE, encoding='utf-8'))
        return float(d.get('last_publish', 0))
    except Exception:
        return 0.0


def _mark(ts):
    try:
        os.makedirs(os.path.dirname(STATE), exist_ok=True)
        json.dump(dict(last_publish=ts), open(STATE, 'w', encoding='utf-8'))
    except Exception:
        pass


def _decision_topic():
    """YC1: lay topic tu decision B neu co."""
    try:
        from ops import decision_to_publish as dtp
        plan = dtp.choose(3)
        for p in plan:
            foot = p.get('footage')
            if foot:
                return foot, p
    except Exception as e:
        _log('decision_topic error: ' + str(e))
    return None, None


def main():
    now = time.time()
    if now - _last_ts() < COOLDOWN:
        _log('cooldown active, skip')
        return 0
    try:
        from ops.auto_publish import run
        dec_topic, dec = _decision_topic()
        if dec_topic:
            _log('decision B topic: ' + str(dec_topic) + ' decisionId=' + str((dec or {}).get('decisionId')))
            r = run(topic=dec_topic, target_dur=14.0)
        else:
            _log('no decision B, fallback topic_picker')
            r = run(target_dur=14.0)
        _log('result: ' + json.dumps(dict(ok=r.get('ok'), topic=r.get('topic'), id=r.get('youtube_id'), err=r.get('error')), ensure_ascii=False))
        if r.get('youtube_id'):
            _mark(now)
    except Exception as e:
        _log('error: ' + str(e))
    return 0


if __name__ == '__main__':
    main()
