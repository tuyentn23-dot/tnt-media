p = 'ops/live_content.py'
b = open(p, 'rb').read()
u = bytes([95])
b = b.replace(b'def strip_html', b'def ' + u + b'strip_html')
b = b.replace(b'= strip_html(', b'= ' + u + b'strip_html(')
open(p, 'wb').write(b)
print('fixed')
