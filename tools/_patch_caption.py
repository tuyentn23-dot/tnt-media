# -- coding: utf-8 --
# Nâng cấp caption channel_style: chữ nhỏ, đặt thấp, nền mờ, không che hình
import io
P = 'ops/channel_style.py'
s = io.open(P, encoding='utf-8').read()
T = chr(9); NL = chr(10); Q = chr(34)
old_y = T + 'y = int(H * 0.35)'
new_y = (T + '# Caption dat thap (vung an toan duoi), chu nho, khong che hinh' + NL
 + T + 'y = int(H * 0.68)')
if old_y in s:
 s = s.replace(old_y, new_y, 1)
 print('patched y ->0.68')
else:
 print('y not found')
# giam font size cho cac scene
old_fs = T + 'fs = int(style.get(' + Q + 'font_size' + Q + ', 70))'
new_fs = T + 'fs = int(style.get(' + Q + 'font_size' + Q + ', 44)) # nho lai cho caption duoi'
if old_fs in s:
 s = s.replace(old_fs, new_fs, 1)
 print('patched fs default 44')
else:
 print('fs not found')
io.open(P, 'w', encoding='utf-8').write(s)
print('written')
