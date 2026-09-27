p = 'pipeline/runner.py'
b = open(p, 'rb').read()
star = bytes([42])
b = b.replace(b'def _call(modname, fnname, args, **kw):', b'def _call(modname, fnname, ' + star + b'args, ' + star + star + b'kw):')
b = b.replace(b'if fn: return fn(args, **kw)', b'if fn: return fn(' + star + b'args, ' + star + star + b'kw)')
open(p, 'wb').write(b)
print('fixed *args')
