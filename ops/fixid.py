p = 'ops/live_content.py'
b = open(p, 'rb').read()
u = bytes([95])
b = b.replace(b"'live' + kind + '" + u + b"' + " + u + b"slug