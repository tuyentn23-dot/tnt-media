# -*- coding: utf-8 -*-
# ops/multichannel_runner.py - Chay auto-publish cho NHIEU kenh enabled
import os, sys, time, json, io
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)
os.environ.setdefault('IMAGEIO_FFMPEG_EXE', os.path.join(ROOT, 'tools', 'ffmpeg.exe'))

from ops import channel_loader as ch
from ops import content_freshness as cf
from ops import channel_style as cs
from ops import os_publish

STATE = os.path.join(ROOT, 'memory', 'multichannel_state.json')
LOG = os.path.join(ROOT, 'logs', 'multichannel.log')

def _log(msg):
    os.makedirs(os.path.dirname(LOG), exist_ok=True)
    line = time.strftime('%Y-%m-%d %H:%M:%S') + ' ' + str(msg)
    with io.open(LOG, 'a', encoding='utf-8') as f:
        f.write(line + chr(10))

def _load_state():
    if os.path.exists(STATE):
        try:
            return json.load(io.open(STATE, encoding='utf-8'))
        except Exception:
            pass
    return {'last_run': {}, 'cycle': 0}

def _save_state(s):
    os.makedirs(os.path.dirname(STATE), exist_ok=True)
    io.open(STATE, 'w', encoding='utf-8').write(json.dumps(s, ensure_ascii=False, indent=2))

def publish_one_channel(cid, per_channel=2):
    cfg = ch.load(cid)
    if not cfg.get('enabled', False):
        return {'ok': False, 'reason': 'disabled', 'id': cid}
    style = cfg.get('style', {})
    kinds = cfg.get('content', {}).get('kinds', [])
    cf.set_channel(cid)
    os_publish.set_channel(cid)
    picks = []
    for kind in kinds:
        items = ch.load_content(cid, kind)
        fresh = [it for it in items if not cf.is_published(cf.signature(it, kind))]
        picks.extend([(kind, it) for it in fresh[:1]])
    picks = picks[:per_channel]
    done = []
    for kind, item in picks:
        out = os.path.abspath('output/ch' + cid + '_' + item['id'] + '_' + time.strftime('%Y%m%d_%H%M%S') + '.mp4')
        os.makedirs(os.path.dirname(out), exist_ok=True)
        try:
            cs.build_styled(item, out, style=style)
        except Exception as e:
            _log('build ERR ' + cid + ' ' + item['id'] + ' ' + str(e)[:120])
            continue
        if os.path.getsize(out) < 300000:
            _log('skip small ' + cid + ' ' + item['id'])
            continue
        c = cfg.get('content', {})
        title = (item.get('hook') or item['id'])[:100]
        desc = ((item.get('body', '') + ' ' + item.get('payoff', ''))[:450])
        tags = list(c.get('tags_base', [])) + [item.get('topic', ''), cid]
        topic = 'ch' + cid + '_' + kind + '_' + item['id']
        res = os_publish.publish(out, title, description=desc, tags=tags, privacy='public', topic=topic, category_id=str(c.get('category_id', '24')), force=True)
        if isinstance(res, dict) and res.get('ok'):
            cf.mark_published(cf.signature(item, kind), {'youtube_id': res.get('youtube_id'), 'topic': topic, 'kind': kind, 'file': out})
            done.append({'id': item['id'], 'yt': res.get('youtube_id')})
            _log('PUBLISHED ' + cid + ' ' + item['id'] + ' ' + str(res.get('youtube_id')))
        else:
            _log('publish blocked ' + cid + ' ' + item['id'] + ' ' + json.dumps(res, ensure_ascii=False)[:150])
    return {'ok': True, 'id': cid, 'published': done}

def run_all(per_channel=2, cooldown_min=180):
    st = _load_state()
    now = time.time()
    results = []
    for cid in ch.list_channels():
        cfg = ch.load(cid)
        if not cfg.get('enabled', False):
            continue
        last = st['last_run'].get(cid, 0)
        if now - last < cooldown_min * 60:
            results.append({'id': cid, 'skip': 'cooldown'})
            continue
        try:
            r = publish_one_channel(cid, per_channel=per_channel)
        except Exception as e:
            r = {'id': cid, 'error': str(e)[:150]}
        results.append(r)
        st['last_run'][cid] = time.time()
        st['cycle'] = st.get('cycle', 0) + 1
        _save_state(st)
    return results

if __name__ == '__main__':
    per = int(sys.argv[1]) if len(sys.argv) > 1 else 2
    print(json.dumps(run_all(per_channel=per), ensure_ascii=True, indent=1))
