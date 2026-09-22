# -*- coding: utf-8 -*-
import io
P='os_app/router.py'
s=io.open(P,encoding='utf-8').read()
api = (
 "\n\n@router.get(\"/api/gallery\")\n"
 "def gallery(limit: int = 60):\n"
 "    import os, glob, time\n"
 "    out = []\n"
 "    d = os.path.join(PKG_ROOT, 'output')\n"
 "    if os.path.isdir(d):\n"
 "        files = sorted(glob.glob(os.path.join(d, '*.mp4')), key=lambda p: os.path.getmtime(p), reverse=True)\n"
 "        for p in files[:limit]:\n"
 "            try:\n"
 "                sz = os.path.getsize(p)\n"
 "            except Exception:\n"
 "                sz = 0\n"
 "            out.append({'name': os.path.basename(p), 'size': sz, 'mtime': os.path.getmtime(p), 'url': '/os/file/' + os.path.basename(p)})\n"
 "    return JSONResponse({'items': out})\n"
 "\n\n@router.get(\"/file/{name}\")\n"
 "def serve_file(name: str):\n"
 "    import os\n"
 "    from fastapi.responses import FileResponse\n"
 "    p = os.path.join(PKG_ROOT, 'output', os.path.basename(name))\n"
 "    if not os.path.exists(p):\n"
 "        return JSONResponse({'ok': False, 'error': 'not found'}, status_code=404)\n"
 "    return FileResponse(p, media_type='video/mp4')\n"
)
if '/api/gallery' in s:
    print('already')
else:
    s2 = s.rstrip() + api + chr(10)
    io.open(P,'w',encoding='utf-8').write(s2)
    import ast
    ast.parse(s2)
    print('gallery API added + syntax OK')
