import sys
sys.path.insert(0,'.')
try:
    from os_app.router import router
    print('router import OK, routes=', len(router.routes))
except Exception as e:
    import traceback
    print('ROUTER ERR:')
    print(traceback.format_exc()[-800:])
