p = 'ops/live_content.py'
b = open(p, 'rb').read()
u = bytes([95])
Q = bytes([39])
b = b.replace(Q + b'live' + Q + b' + kind + ' + Q + u + Q, Q + b'live' + u + Q + b' + kind + ' + Q + u + Q)
open(p, 'wb').write(b)
print('fixed')
