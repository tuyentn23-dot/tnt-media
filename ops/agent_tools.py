# -*- coding: utf-8 -*-
# ops/agent_tools.py - Cong cu mo rong cho agent: mo web, chup man hinh, nhat ky hanh dong
import os, sys, json, io, time, subprocess, webbrowser
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ACTIONS_LOG = os.path.join(ROOT, 'memory', 'agent_actions.jsonl')

def _log(action, detail):
    os.makedirs(os.path.dirname(ACTIONS_LOG), exist_ok=True)
    rec = {'ts': time.strftime('%Y-%m-%d %H:%M:%S'), 'action': action, 'detail': detail}
    with io.open(ACTIONS_LOG, 'a', encoding='utf-8') as f:
        f.write(json.dumps(rec, ensure_ascii=False) + chr(10))
    return rec

def open_url(url):
    """Mo URL trong trinh duyet mac dinh."""
    if not url.startswith('http'):
        url = 'http://' + url
    try:
        webbrowser.open(url)
        _log('open_url', url)
        return {'ok': True, 'url': url}
    except Exception as e:
        return {'ok': False, 'error': str(e)[:150]}

def screenshot(path=None):
    """Chup man hinh, luu vao output/screenshots."""
    if not path:
        d = os.path.join(ROOT, 'output', 'screenshots')
        os.makedirs(d, exist_ok=True)
        path = os.path.join(d, 'shot_' + time.strftime('%Y%m%d_%H%M%S') + '.png')
    try:
        from PIL import ImageGrab
        img = ImageGrab.grab()
        img.save(path)
        _log('screenshot', path)
        return {'ok': True, 'path': path, 'size': img.size}
    except Exception as e:
        try:
            import pyautogui
            img = pyautogui.screenshot()
            img.save(path)
            _log('screenshot', path)
            return {'ok': True, 'path': path, 'size': img.size}
        except Exception as e2:
            return {'ok': False, 'error': str(e)[:100] + ' | ' + str(e2)[:100]}

def list_actions(limit=50):
    """Xem nhat ky hanh dong da lam."""
    if not os.path.exists(ACTIONS_LOG):
        return []
    lines = io.open(ACTIONS_LOG, encoding='utf-8').read().strip().split(chr(10))
    out = []
    for l in lines[-limit:]:
        try:
            out.append(json.loads(l))
        except Exception:
            pass
    return list(reversed(out))

def run_cmd(cmd, timeout=30):
    """Chay lenh shell an toan (gioi han)."""
    try:
        r = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=timeout, encoding='utf-8', errors='replace')
        _log('run_cmd', cmd[:200])
        return {'ok': True, 'stdout': (r.stdout or '')[:5000], 'stderr': (r.stderr or '')[:2000], 'code': r.returncode}
    except Exception as e:
        return {'ok': False, 'error': str(e)[:200]}

def read_screen_text():
    """Doc chu tren man hinh (OCR neu co)."""
    try:
        import pyautogui, pytesseract
        from PIL import Image
        img = pyautogui.screenshot()
        txt = pytesseract.image_to_string(img)
        _log('read_screen_text', 'len=' + str(len(txt)))
        return {'ok': True, 'text': txt[:5000]}
    except Exception as e:
        return {'ok': False, 'error': str(e)[:200]}

if __name__ == '__main__':
    print(json.dumps({'actions': list_actions(10)}, ensure_ascii=True, indent=1))
