p = 'ops/live_content.py'
b = open(p, 'rb').read()
u = bytes([95])
Q = bytes([39])
old1 = b"'live'"
old2 = b"kind"
old3 = b"''"
old4 = u + b"slug"
new = Q + b'live' + Q + b' + kind + ' + Q + u + Q + b' + ' + u + b'slug'
b = b.replace(Q + b'live' + Q + b' + kind + ' + Q + Q + b' + ' + u + b'slug', Q + b'live' + Q + b' + kind + ' + Q + u + Q + b' + ' + u + b'slug')
open(p, 'wb').write(b)
print('done')
