import os, sys, json, time, threading, sqlite3
from datetime import datetime

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)
os.chdir(ROOT)
os.environ.setdefault('IMAGEIO_FFMPEG_EXE', os.path.join(ROOT, 'tools', 'ffmpeg.exe'))
STATE = os.path.join(ROOT, 'memory', 'tray_state.json')
DB = os.path.join(ROOT, 'system', 'state.db')
LOG = os.path.join(ROOT, 'logs', 'tray_app.log')

def log(msg):
    try:
        os.makedirs(os.path.dirname(LOG), exist_ok=True)
        f = open(LOG, 'a', encoding='utf-8')
        f.write(datetime.now().strftime('%Y-%m-%d %H:%M:%S ') + str(msg) + chr(10))
        f.close()
    except Exception:
        pass

def load_state():
    d = {'paused': False, 'last_run': {}, 'cycle': 0, 'fired': {}}
    if os.path.exists(STATE):
        d.update(json.load(open(STATE, encoding='utf-8')))
    return d

def save_state(s):
    os.makedirs(os.path.dirname(STATE), exist_ok=True)
    json.dump(s, open(STATE, 'w', encoding='utf-8'), ensure_ascii=False, indent=2)
def channels():
    con = sqlite3.connect(DB)
    rows = list(con.execute('SELECT name, scheduleCron FROM channels WHERE active=1'))
    con.close()
    return rows

def hours_from_cron(expr):
    p = (expr or '').split()
    if len(p) != 5:
        return []
    out = []
    for part in p[1].split(','):
        out.append(int(part))
    return out

def due_channels(now, fired):
    slot = now.strftime('%Y%m%d%H')
    out = []
    for name, cron in channels():
        if now.hour not in hours_from_cron(cron):
            continue
        k = name + '|' + slot
        if fired.get(k):
            continue
        out.append((name, k))
    return out

def do_publish(name, limit):
    from ops import multichannel_runner as mr
    return mr.publish_one_channel(name, per_channel=limit)
def next_run_text(st):
    lr = st.get('last_run') or {}
    t = max(lr.values()) if lr else 0
    s = time.strftime('%H:%M', time.localtime(t)) if t else 'never'
    return 'Last: ' + s + ' | cycle ' + str(st.get('cycle', 0))

def worker_loop(stop_event, ref):
    while not stop_event.is_set():
        st = load_state()
        if not st.get('paused'):
            try:
                now = datetime.now()
                due = due_channels(now, st.get('fired', {}))
                for name, k in due:
                    res = do_publish(name, 4)
                    st.setdefault('fired', {})[k] = True
                    st.setdefault('last_run', {})[name] = time.time()
                    st['cycle'] = st.get('cycle', 0) + 1
                    save_state(st)
                    log('PUBLISH ' + name + ' ' + json.dumps(res, ensure_ascii=True)[:200])
                slot = now.strftime('%Y%m%d%H')
                st['fired'] = {kk: vv for kk, vv in st.get('fired', {}).items() if kk.endswith(slot)}
            except Exception as e:
                log('ERROR ' + str(e))
        ic = ref.get('icon')
        if ic:
            try:
                ic.title = 'TNT Media OS | ' + next_run_text(st)
            except Exception:
                pass
        for _ in range(300):
            if stop_event.is_set():
                return
            time.sleep(1)
def make_image():
    from PIL import Image, ImageDraw
    img = Image.new('RGBA', (64, 64), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    d.ellipse((4, 4, 60, 60), fill=(168, 85, 247, 255))
    d.text((20, 24), 'TNT', fill=(255, 255, 255, 255))
    return img

def main():
    import pystray
    from pystray import MenuItem as MI, Menu as M
    stop_event = threading.Event()
    ref = {}
    t = threading.Thread(target=worker_loop, args=(stop_event, ref), daemon=True)
    t.start()
    def on_run(icon, item):
        st = load_state()
        names = [n for n, c in channels()]
        for n in names:
         res = do_publish(n, 4)
         log('MANUAL ' + n + ' ' + json.dumps(res, ensure_ascii=True)[:150])
    def on_pause(icon, item):
        st = load_state()
        st['paused'] = not st.get('paused', False)
        save_state(st)
        log('paused=' + str(st['paused']))
    def on_dash(icon, item):
        os.startfile(os.path.join(ROOT, '_serve.py'))
    def on_logs(icon, item):
        os.startfile(LOG)
    def on_quit(icon, item):
        stop_event.set()
        icon.stop()
    menu = M(
        MI('Run now (4/kenh)', on_run),
        MI('Pause / Resume', on_pause),
        MI('Open dashboard', on_dash),
        MI('Open logs', on_logs),
        MI('Quit', on_quit),
    )
    icon = pystray.Icon('tnt_media', make_image(), 'TNT Media OS', menu)
    ref['icon'] = icon
    log('tray start')
    icon.run()

if __name__ == '__main__':
    main()
