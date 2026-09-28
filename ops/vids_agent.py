# -- coding: utf-8 --
# Google Vids AI video generator (free, no API key).
# YEU CAU: Chrome chay --remote-debugging-port=9222, da dang nhap Google (dung launch_chrome.py).
# Dung: from ops import vids_agent; r = vids_agent.generate(prompt, out_path)
# Xem ops/MODULES.md (section vids_agent.py) de biet chi tiet + bai hoc.
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
    port = pg.get_by_text('Create a portrait video')
    if port.count() > 0:
     port.first.click()
     pg.wait_for_timeout(7000)
    pg.wait_for_timeout(7000)
    return pg

def _cdp_click(pg, locator):
    """Click qua CDP Input.dispatchMouseEvent - bo qua actionability check (tranh treo)."""
    bb = locator.bounding_box()
    if not bb:
     return False
    cx = bb['x'] + bb['width'] / 2
    cy = bb['y'] + bb['height'] / 2
    pg.mouse.move(cx, cy)
    pg.wait_for_timeout(200)
    pg.mouse.click(cx, cy)
    return True

def _js_click(pg, text):
    js = '(t)=>{const ms=[...document.querySelectorAll("[role=menuitem],button,div[role=button]")];const m=ms.find(e=>e.textContent.trim()===t||e.textContent.trim().startsWith(t));if(m){m.click();return 1}return 0}'
    return pg.evaluate(js, text)

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

def _set_portrait(pg):
    s = pg.locator('button[aria-label*="Generation settings"]')
    if s.count() > 0:
     _cdp_click(pg, s.first)
     pg.wait_for_timeout(1500)
    port = pg.locator('text=Portrait')
    if port.count() > 0:
     _cdp_click(pg, port.last)
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

def _download(pg, dl_dir):
    b = pg.context.browser
    bcdp = b.new_browser_cdp_session()
    bcdp.send('Browser.setDownloadBehavior', {'behavior': 'allow', 'downloadPath': dl_dir, 'eventsEnabled': True})
    pg.keyboard.press('Escape')
    pg.wait_for_timeout(800)
    mi = pg.locator('[role=menubar] [role=menuitem]')
    _cdp_click(pg, mi.nth(0))
    pg.wait_for_timeout(1500)
    d = pg.locator('[role=menuitem]:has-text("Download")')
    d.last.hover(timeout=5000)
    pg.wait_for_timeout(2500)
    m = pg.locator('[role=menuitem]:has-text("MP4")')
    return _cdp_click(pg, m.last)

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

def _insert_video(pg):
    ins = pg.locator('button:has-text("Insert")')
    if ins.count() > 0:
        _cdp_click(pg, ins.first)
        pg.wait_for_timeout(5000)
        return True
    return False

def _to_portrait(path, w=1080, h=1920):
    import subprocess, shutil, os
    root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    ff = os.path.join(root, 'tools', 'ffmpeg.exe')
    if not os.path.exists(ff):
     ff = 'ffmpeg'
    tmp = path + '.portrait.mp4'
    vf = 'scale='+str(w)+':'+str(h)+':force_original_aspect_ratio=decrease,pad='+str(w)+':'+str(h)+':(ow-iw)/2:(oh-ih)/2:color=black'
    cmd = [ff, '-y', '-i', path, '-vf', vf, '-c:a', 'copy', tmp]
    r = subprocess.run(cmd, capture_output=True)
    if r.returncode == 0 and os.path.exists(tmp):
     shutil.move(tmp, path)
     return True
    return False

def generate(prompt, out_path, cdp_url=None, reuse_page=False, keep_page=False):
    from playwright.sync_api import sync_playwright
    dl_dir = os.path.dirname(os.path.abspath(out_path)) or '.'
    os.makedirs(dl_dir, exist_ok=True)
    for f in os.listdir(dl_dir):
     if f.endswith('.mp4'):
      try: os.remove(os.path.join(dl_dir, f))
      except Exception: pass
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
         _set_portrait(pg)
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
         res['ok'] = True
         res['path'] = os.path.abspath(out_path)
        finally:
         if created and not keep_page:
          try: pg.close()
          except Exception: pass
    return res
