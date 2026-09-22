import sys, os, json, time
ROOT = os.getcwd()
sys.path.insert(0, ROOT)
def topics_for(channel):
    j = json.load(open(os.path.join('channels', channel + '.json'), encoding='utf-8'))
    return j.get('topics') or []
def main():
    ch = sys.argv[1]
    privacy = sys.argv[2] if len(sys.argv) > 2 else 'unlisted'
    per = int(sys.argv[3]) if len(sys.argv) > 3 else 4
    from ops import os_publish
    from ops.auto_publish import run
    os_publish.set_channel(ch)
    pool = topics_for(ch)
    print('CHANNEL', ch, 'POOL', pool, flush=True)
    ok = 0
    for i in range(per):
        topic = pool[i % len(pool)]
        res = False
        yid = None
        err = None
        for attempt in range(2):
            try:
                r = run(topic=topic, target_dur=14.0, privacy=privacy, allow_republish=True)
                res = r.get('ok')
                yid = r.get('youtube_id')
                err = r.get('error')
            except Exception as ex:
                res = False
                err = repr(ex)[:150]
            if res:
                break
            time.sleep(3)
        ee = str(err).encode('ascii','replace').decode() if err else ''
        print('CLIP', ch, i+1, topic, 'ok=', res, 'id=', yid, 'err=', ee, flush=True)
        if res:
            ok = ok + 1
        time.sleep(2)
    print('DONE', ch, 'ok=', ok, flush=True)
if __name__ == '__main__':
    main()
