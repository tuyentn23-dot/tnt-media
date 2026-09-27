# CAC LOI HIGH - DA XAC MINH

## 2.4. [HIGH] Render dong thoi lan caption

File: ops/ffmpeg_render.py dong 146 va 171
Bang chung da xac minh:

tmp = '_work'; os.makedirs(tmp, exist_ok=True)

(hai cho, dung chung _work)

Hau qua: 2 job song song ghi de _work/c0.txt, _work/hook.txt -> caption sai.

Sua:
python
import tempfile, shutil
base = os.path.join(ROOT, '_work')
os.makedirs(base, exist_ok=True)
tmp = tempfile.mkdtemp(prefix='render_', dir=base)
try:
 # ... render ...
finally:
 shutil.rmtree(tmp, ignore_errors=True)


## 2.5. [HIGH] Renderer tra tuple loi nhung wrapper bo qua

File: modules/render/video.py dong 24: return out khong kiem tra ket qua
Hau qua: FFmpeg that bai nhung runner tuong thanh cong
Sua: Wrapper kiem tra ket qua render() that, raise exception neu fail.

## 2.6. [HIGH] Backup API UI dung cach cu

File: app/server.py dong 358-359
Bang chung da xac minh: @app.post('/api/backup') def backup(): dung shutil.copy2
Sua: Doi API goi ops/backup_state.py (SQLite Backup API).

## 2.7. [HIGH] Runner van fallback channel_style (hong)

File: pipeline/runner.py dong 88-89
Bang chung da xac minh:

from ops import channel_style as cs
cs.build_styled(item, out, style=style)

Sua: Bo fallback hoac sua channel_style (xem 5.1).

## 2.8. [HIGH] Tray pause/resume anh huong tat ca kenh

File: app/tray.py dong 185
Bang chung da xac minh: UPDATE channels SET enabled=0 (tat ca kenh)
on_resume: UPDATE channels SET enabled=1 (bat ca kenh vua tat thu cong)
Sua: Tach trang thai pause he thong khoi enabled kenh. Dung file flag state/paused.flag.

## 2.9. [HIGH] Tray cac van de khac

- "Trang thai" chi in console -> pythonw khong thay
- "Mo" khi browser con song khong bring to front
- "Xem loi" -> mo Dashboard (khong phai log loi)
- "Khoi phuc ket noi" -> neu server song nhung treo, spawn_server tra True (port mo)
- "Thoat" -> chua kill runner con
- "Dung khan cap" -> chi doi DB status

## 2.10. [HIGH] Giao dien 7777 loi cu

File: app/ui/index.html
- Dong ~95: loi dau nhay tai truong thoi gian va log
- Refresh All tao them interval
- Che do approve/auto chi doi bien UI, khong luu/apply
- Khong co player xem/nghe video truoc khi duyet
- Phu thuoc CDN
- 13 tab, cau truc cu
