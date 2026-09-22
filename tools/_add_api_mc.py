# -*- coding: utf-8 -*-
import io
P = 'os_app/router.py'
s = io.open(P, encoding='utf-8').read()
api = (
"\n\n@router.post(\"/api/multichannel/run\")\n"
"def multichannel_run(per_channel: int = 2):\n"
"    from ops.multichannel_runner import run_all\n"
"    try:\n"
"        return JSONResponse({\"items\": run_all(per_channel=per_channel)})\n"
"    except Exception as e:\n"
"        return JSONResponse({\"ok\": False, \"error\": str(e)[:200]})\n"
"\n\n@router.get(\"/api/multichannel/state\")\n"
"def multichannel_state():\n"
"    import json, os\n"
"    p = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'memory', 'multichannel_state.json')\n"
"    if os.path.exists(p):\n"
"        try:\n"
"            return JSONResponse(json.loads(open(p, encoding='utf-8').read()))\n"
"        except Exception as e:\n"
"            return JSONResponse({\"error\": str(e)})\n"
"    return JSONResponse({\"cycle\": 0, \"last_run\": {}})\n"
"\n\n@router.get(\"/api/video/health\")\n"
"def video_health_api(path: str):\n"
"    from ops.video_health import check\n"
"    return JSONResponse(check(path))\n"
)
if 'multichannel/run' in s:
    print('already patched')
else:
    s2 = s.rstrip() + api + chr(10)
    io.open(P, 'w', encoding='utf-8').write(s2)
    import ast
    ast.parse(s2)
    print('patched router + syntax OK')
