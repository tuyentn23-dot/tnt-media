# -*- coding: utf-8 -*-
import io
P='os_app/router.py'
s=io.open(P,encoding='utf-8').read()
api = (
 "\n\n@router.post(\"/api/agent/open_url\")\n"
 "def agent_open_url(url: str):\n"
 "    from ops import agent_tools as at\n"
 "    return JSONResponse(at.open_url(url))\n"
 "\n\n@router.post(\"/api/agent/screenshot\")\n"
 "def agent_screenshot():\n"
 "    from ops import agent_tools as at\n"
 "    return JSONResponse(at.screenshot())\n"
 "\n\n@router.get(\"/api/agent/actions\")\n"
 "def agent_actions(limit: int = 50):\n"
 "    from ops import agent_tools as at\n"
 "    return JSONResponse({\"items\": at.list_actions(limit)})\n"
 "\n\n@router.post(\"/api/agent/run_cmd\")\n"
 "def agent_run_cmd(cmd: str, timeout: int = 30):\n"
 "    from ops import agent_tools as at\n"
 "    return JSONResponse(at.run_cmd(cmd, timeout=timeout))\n"
 "\n\n@router.post(\"/api/agent/read_screen\")\n"
 "def agent_read_screen():\n"
 "    from ops import agent_tools as at\n"
 "    return JSONResponse(at.read_screen_text())\n"
)
if '/api/agent/open_url' in s:
    print('already')
else:
    s2 = s.rstrip() + api + chr(10)
    io.open(P,'w',encoding='utf-8').write(s2)
    import ast
    ast.parse(s2)
    print('agent API added + syntax OK')
