# -- coding: utf-8 --
# Google Vids AI video generator (free, no API key).
import os, time
CDP_URL = os.environ.get('TNT_VIDS_CDP', 'http://127.0.0.1:9222')
CREATE_URL = 'https://docs.google.com/videos/create'
VIDS_MATCH = 'docs.google.com/videos'

def _first_page(ctx):
    for page in ctx.pages:
        if VIDS_MATCH in page.url:
            return page
    return None

def _new_project(ctx):
    pg = ctx.new_page()
    pg.goto(CREATE_URL, wait_until='domcontentloaded', timeout=45000)
    pg.wait_for_timeout(7000)
    pb = pg.locator('button:has-text("Portrait")')
    if pb.count() > 0:
        bb = pb.first.bounding_box()
        if bb:
            pg.mouse.click(bb['x'] + bb['width'] / 2, bb['y'] + bb['height'] / 2)
            pg.wait_for_timeout(8000)
    return pg

def _cdp_click(pg, locator):
    bb = locator.bounding_box()
    if not bb:
        return False
    cx = bb['x'] + bb['width'] / 2
    cy = bb['y'] + bb['height'] / 2
    pg.mouse.move(cx, cy)
    pg.wait_for_timeout(200)
    pg.mouse.click(cx, cy)
    return True

def _open_ai_panel(pg):
    btn = pg.locator('button:has-text("Create AI videos")')
    if btn.count() > 0:
        _cdp_click(pg, btn.first)
        pg.wait_for_timeout(3000)
    sc = pg.get_by_text('Create from scratch')
    if sc.count() > 0:
        _cdp_click(pg, sc.first)
        pg.wait_for_timeout(2000)
    return True

def _fill_prompt(pg, prompt):
    ce = pg.locator('[contenteditable="true"]')
    if ce.count() == 0:
        return False
    _cdp_click(pg, ce.last)
    pg.wait_for_timeout(500)
    ce.last.type(prompt, delay=8)
    pg.wait_for_timeout(1200)
    return True

def _click_generate(pg):
    g = pg.locator('button[aria-label="Generate"]')
    if g.count() > 0:
        return _cdp_click(pg, g.first)
    return False

def _wait_video(pg, timeout=300):
    t0 = time.time()
    while time.time() - t0 < timeout:
        n = pg.locator('button:has-text("Insert")').count()
        if n > 0:
            return True
        pg.wait_for_timeout(4000)
    return False

def _insert_video(pg):
    ins = pg.locator('button:has-text("Insert")')
    if ins.count() > 0:
        _cdp_click(pg, ins.first)
        pg.wait_for_timeout(5000)
        return True
    return False

def _download(pg, dl_dir):
    b = pg.context.browser
    bcdp = b.new_browser_cdp_session()
    bcdp.send('Browser.setDownloadBehavior', {'behavior': 'allow', 'downloadPath': dl_dir, 'eventsEnabled': True})
    captured = {}
    def _on_req(r):
        u = r.url
        if 'download' in u or 'videoplayback' in u or 'alt=media' in u:
            try:
                captured['url'] = u
                captured['headers'] = r.all_headers()
            except Exception:
                pass
    pg.on('request', _on_req)
    for attempt in range(3):
        pg.keyboard.press('Escape')
        pg.wait_for_timeout(800)
        mi = pg.locator('[role=menubar] [role=menuitem]')
        _cdp_click(pg, mi.nth(0))
        pg.wait_for_timeout(1500)
        d = pg.locator('[role=menuitem]:has-text("Download")')
        if d.count() == 0:
            pg.wait_for_timeout(1000)
            continue
        d.last.hover(timeout=5000)
        pg.wait_for_timeout(2500)
        m = pg.locator('[role=menuitem]:has-text("MP4")')
        if m.count() == 0:
            continue
        _cdp_click(pg, m.last)
        pg.wait_for_timeout(6000)
        fs = [f for f in os.listdir(dl_dir) if f.endswith(chr(46)+chr(109)+chr(112)+chr(52))]
        if fs:
            pg.remove_listener('request', _on_req)
            return True
        if captured.get('url'):
            try:
                import requests
                rr = requests.get(captured['url'], headers=captured.get('headers') or {}, stream=True, timeout=120)
                if rr.status_code == 200:
                    fp = os.path.join(dl_dir, 'dl_replay.mp4')
                    with open(fp, 'wb') as fh:
                        for chunk in rr.iter_content(65536):
                            fh.write(chunk)
                    pg.remove_listener('request', _on_req)
                    return True
            except Exception:
                pass
        pg.wait_for_timeout(2000)
    try:
        pg.remove_listener('request', _on_req)
    except Exception:
        pass
    return False

def _wait_file(dl_dir, timeout=180):
    t0 = time.time()
    while time.time() - t0 < timeout:
        fs = [f for f in os.listdir(dl_dir) if f.endswith('.mp4')]
        if fs:
            p = os.path.join(dl_dir, fs[0])
            s1 = os.path.getsize(p)
            time.sleep(3)
            if os.path.getsize(p) == s1:
                return p
        time.sleep(2)
    return None

def _to_portrait(path, w=1080, h=1920):
    import subprocess, shutil, os
    root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    ff = os.path.join(root, 'tools', 'ffmpeg.exe')
    if not os.path.exists(ff):
        ff = 'ffmpeg'
    tmp = path + '.portrait.mp4'
    vf = 'scale=' + str(w) + ':' + str(h) + ':force_original_aspect_ratio=decrease,pad=' + str(w) + ':' + str(h) + ':(ow-iw)/2:(oh-ih)/2:color=black'
    cmd = [ff, '-y', '-i', path, '-vf', vf, '-c:a', 'copy', tmp]
    r = subprocess.run(cmd, capture_output=True)
    if r.returncode == 0 and os.path.exists(tmp):
        shutil.move(tmp, path)
        return True
    return False

def _add_caption(path, lines, hook=None):
    import subprocess, shutil, os
    root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    ff = os.path.join(root, 'tools', 'ffmpeg.exe')
    if not os.path.exists(ff):
        ff = 'ffmpeg'
    d = os.path.dirname(path)
    dur = 10.0
    segs = []
    if hook:
        segs.append((0.0, 3.0, hook))
    if lines:
        n = len(lines)
        base = 3.0 if hook else 0.0
        seg = (dur - base) / n
        for i, ln in enumerate(lines):
            segs.append((base + i * seg, base + (i + 1) * seg, str(ln)))
    if not segs:
        return False
    def _ts(t):
        h = int(t // 3600)
        m = int((t % 3600) // 60)
        sec = t % 60
        return str(h).zfill(2) + ':' + str(m).zfill(2) + ':' + ('%06.3f' % sec).replace('.', ',')
    srt = []
    for i, (x, y, tx) in enumerate(segs, 1):
        srt.append(str(i))
        srt.append(_ts(x) + ' --> ' + _ts(y))
        srt.append(tx)
        srt.append('')
    sf = os.path.join(d, '_sub.srt')
    open(sf, 'w', encoding='utf-8').write(chr(10).join(srt))
    tmp = path + '.cap.mp4'
    srt_esc = sf.replace(chr(92), '/').replace(':', chr(92) + ':')
    style = 'FontName=Arial,FontSize=15,Bold=1,PrimaryColour=&H00FFFFFF,OutlineColour=&H00000000,BackColour=&H00000000,BorderStyle=1,Outline=2,Shadow=1,MarginV=100,Alignment=2'
    vf = 'subtitles=' + srt_esc + ':force_style=' + chr(39) + style + chr(39)
    cmd = [ff, '-y', '-i', path, '-vf', vf, '-c:a', 'copy', tmp]
    r = subprocess.run(cmd, capture_output=True)
    if r.returncode == 0 and os.path.exists(tmp):
        shutil.move(tmp, path)
        return True
    return False

def _add_voice(path, voice_text, voice_name=None):
    import subprocess, shutil, os
    root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    ff = os.path.join(root, 'tools', 'ffmpeg.exe')
    if not os.path.exists(ff):
        ff = 'ffmpeg'
    if not voice_text:
        return False
    try:
        from ops import voice as _v
        vp, sents = _v.synth(voice_text, out_path=os.path.join(os.path.dirname(path), '_vo.mp3'), voice=voice_name)
    except Exception:
        return False
    if not vp or not os.path.exists(vp):
        return False
    tmp = path + '.vo.mp4'
    fc = '[0:a]volume=0.22[bg];[1:a]volume=1.8[vo];[bg][vo]amix=inputs=2:duration=first:dropout_transition=0'
    cmd = [ff, '-y', '-i', path, '-i', vp, '-filter_complex', fc, '-c:v', 'copy', '-c:a', 'aac', '-shortest', tmp]
    r = subprocess.run(cmd, capture_output=True)
    if r.returncode == 0 and os.path.exists(tmp):
        shutil.move(tmp, path)
        return True
    return False
def generate(prompt, out_path, cdp_url=None, reuse_page=False, keep_page=False, captions=None, hook=None, voice_text=None, voice_name=None):
    from playwright.sync_api import sync_playwright
    dl_dir = os.path.join(os.path.dirname(os.path.abspath(out_path)) or '.', '_vids_tmp')
    if os.path.isdir(dl_dir):
        for f in os.listdir(dl_dir):
            try:
                os.remove(os.path.join(dl_dir, f))
            except Exception:
                pass
    os.makedirs(dl_dir, exist_ok=True)
    url = cdp_url or CDP_URL
    res = {'ok': False, 'error': None, 'path': None, 'url': None}
    with sync_playwright() as p:
        b = p.chromium.connect_over_cdp(url)
        ctx = b.contexts[0]
        pg = _first_page(ctx) if reuse_page else None
        created = False
        if pg is None:
            pg = _new_project(ctx)
            created = True
        res['url'] = pg.url
        try:
            _open_ai_panel(pg)
            if not _fill_prompt(pg, prompt):
                res['error'] = 'prompt input not found'
                return res
            if not _click_generate(pg):
                res['error'] = 'generate not found'
                return res
            if not _wait_video(pg, 300):
                res['error'] = 'video not ready'
                return res
            _insert_video(pg)
            _download(pg, dl_dir)
            fp = _wait_file(dl_dir, 180)
            if not fp:
                res['error'] = 'download failed'
                return res
            import shutil
            shutil.move(fp, out_path)
            _to_portrait(out_path)
            if voice_text:
                _add_voice(out_path, voice_text, voice_name)
            if captions or hook:
                _add_caption(out_path, captions or [], hook)
            res['ok'] = True
            res['path'] = os.path.abspath(out_path)
        finally:
            if created and not keep_page:
                try:
                    pg.close()
                except Exception:
                    pass
    return res
