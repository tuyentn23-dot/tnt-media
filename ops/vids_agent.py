# -- coding: utf-8 --
# Google Vids AI video generator (free, no API key).
# Ket noi Chrome that qua CDP (port 9222), tao video AI tu prompt,
# chon Portrait 9:16, Generate, download MP4 ve thu muc chi dinh.
# YEU CAU: Chrome chay voi --remote-debugging-port=9222, da dang nhap Google.
# Dung launch_chrome.py de mo Chrome dung cach.
import os, time
CDP_URL = os.environ.get('TNT_VIDS_CDP', 'http://127.0.0.1:9222')
VIDS_MATCH = 'docs.google.com/videos'

def _find_page(ctx):
    for page in ctx.pages:
        if VIDS_MATCH in page.url:
            return page
    return None

def _download(pg, dl_dir):
    b = pg.context.browser
    bcdp = b.new_browser_cdp_session()
    bcdp.send('Browser.setDownloadBehavior', {'behavior': 'allow', 'downloadPath': dl_dir, 'eventsEnabled': True})
    pg.keyboard.press('Escape')
    pg.wait_for_timeout(800)
    mi = pg.locator('[role=menubar] [role=menuitem]')
    mi.nth(0).click()
    pg.wait_for_timeout(1500)
    d = pg.locator('[role=menuitem]:has-text("Download")')
    d.last.hover(timeout=5000)
    pg.wait_for_timeout(2500)
    m = pg.locator('[role=menuitem]:has-text("MP4")')
    bb = m.last.bounding_box()
    cx = bb['x'] + bb['width'] / 2
    cy = bb['y'] + bb['height'] / 2
    pg.mouse.move(cx, cy)
    pg.wait_for_timeout(500)
    pg.mouse.click(cx, cy)
    return True

def _open_ai_panel(pg):
    btn = pg.locator('button:has-text("Create AI videos")')
    if btn.count() > 0:
        btn.first.click()
        pg.wait_for_timeout(2500)
    scratch = pg.get_by_text('Create from scratch')
    if scratch.count() > 0:
        scratch.first.click()
        pg.wait_for_timeout(1500)
    return True

def _fill_prompt(pg, prompt):
    ce = pg.locator('[contenteditable="true"]')
    ce.last.click()
    ce.last.type(prompt, delay=8)
    pg.wait_for_timeout(1000)
    return True

def _set_portrait(pg):
    s = pg.locator('button[aria-label*="Generation settings"]')
    if s.count() > 0:
        s.first.click(force=True)
        pg.wait_for_timeout(1200)
    port = pg.locator('text=Portrait')
    if port.count() > 0:
        port.last.click(force=True)
        pg.wait_for_timeout(1000)
    return True

def _click_generate(pg):
    g = pg.locator('button[aria-label="Generate"]')
    if g.count() > 0:
        g.first.click(force=True)
        return True
    return False

def _wait_for_video(pg, timeout=240):
    t0 = time.time()
    while time.time() - t0 < timeout:
        ins = pg.locator('button:has-text("Insert video")')
        if ins.count() > 0:
            return True
        pg.wait_for_timeout(3000)
    return False

def _wait_file(dl_dir, timeout=120):
    t0 = time.time()
    while time.time() - t0 < timeout:
        fs = [f for f in os.listdir(dl_dir) if f.endswith('.mp4')]
        if fs:
            return os.path.join(dl_dir, fs[0])
        time.sleep(2)
    return None

def generate(prompt, out_path, cdp_url=None, headless=False):
    from playwright.sync_api import sync_playwright
    dl_dir = os.path.dirname(os.path.abspath(out_path)) or '.'
    os.makedirs(dl_dir, exist_ok=True)
    url = cdp_url or CDP_URL
    result = {'ok': False, 'error': None, 'path': None}
    with sync_playwright() as p:
        b = p.chromium.connect_over_cdp(url)
        ctx = b.contexts[0]
        pg = _find_page(ctx)
        if pg is None:
         result['error'] = 'no Vids page open'
         return result
        _open_ai_panel(pg)
        _fill_prompt(pg, prompt)
        _set_portrait(pg)
        ok = _click_generate(pg)
        if not ok:
         result['error'] = 'generate button not found'
         return result
        ready = _wait_for_video(pg, timeout=300)
        if not ready:
         result['error'] = 'video not ready in time'
         return result
        _download(pg, dl_dir)
        fp = _wait_file(dl_dir, timeout=150)
        if not fp:
         result['error'] = 'download failed'
         return result
        import shutil
        shutil.move(fp, out_path)
        result['ok'] = True
        result['path'] = os.path.abspath(out_path)
    return result
