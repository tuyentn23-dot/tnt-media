P='os_app/router.py'
s=open(P,encoding='utf-8').read()
api=(
'\n\n@router.post("/api/channels/{cid}/publish")\n'
'def channel_publish(cid: str, count: int = 2):\n'
'    from ops.multichannel_runner import publish_one_channel\n'
'    try:\n'
'        return JSONResponse(publish_one_channel(cid, per_channel=count))\n'
'    except Exception as e:\n'
'        return JSONResponse({"ok": False, "error": str(e)[:200]})\n'
'\n\n@router.get("/control", response_class=HTMLResponse)\n'
'def control_page():\n'
'    return _serve("control.html")\n'
)
if 'channels/{cid}/publish' in s:
    print('already')
else:
    s=s.rstrip()+api+chr(10)
    open(P,'w',encoding='utf-8').write(s)
    import ast
    ast.parse(s)
    print('added publish+control route')
