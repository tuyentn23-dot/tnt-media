p = 'ops/live_content.py'
b = open(p, 'rb').read()
u = bytes([95])
Q = bytes([39])
b = b.replace(b"vid = 'live' + kind + '' + " + u + b"slug