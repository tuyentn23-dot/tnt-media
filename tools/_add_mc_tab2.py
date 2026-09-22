# -*- coding: utf-8 -*-
import io, base64
P = 'os_app/ui/index.html'
s = io.open(P, encoding='utf-8', errors='replace').read()
old_tab = "['channels','Kenh','CH','Quan ly kenh'],"
new_tab = old_tab + "['multich','Da kenh','MC','Auto dang nhieu kenh'],"
if 'multich' not in s[:6000]:
    s = s.replace(old_tab, new_tab, 1)
    print('tab added')
else:
    print('tab exists')
fn_b64 = 'YXN5bmMgZnVuY3Rpb24gbXVsdGljaCgpe2NvbnN0IGM9ZG9jdW1lbnQuZ2V0RWxlbWVudEJ5SWQoJ2NvbnRlbnQnKTsKbGV0IGg9JzxkaXYgY2xhc3M9cGFuZWw+PGgyPkF1dG8gZGFuZyBuaGlldSBrZW5oPC9oMj4nO2grPSc8ZGl2IGNsYXNzPXJvdz48YnV0dG9uIGNsYXNzPSJidG4gb2siIG9uY2xpY2s9Im1jUnVuKCkiPkNoYXkgYXV0byBkYW5nPC9idXR0b24+ICc7aCs9JzxidXR0b24gY2xhc3M9ImJ0biIgb25jbGljaz0ibWNTdGF0ZSgpIj5UcmFuZyB0aGFpPC9idXR0b24+PC9kaXY+JztoKz0nPHByZSBpZD0ibWN PdXQiIHN0eWxlPSJ3aGl0ZS1zcGFjZTpwcmUtd3JhcDtmb250LXNpemU6MTJweCI+PC9wcmU+PC9kaXY+JztjLmlubmVySFRNTD1oO21jU3RhdGUoKTt9CmFzeW5jIGZ1bmN0aW9uIG1jUnVuKCl7Y29uc3Qgbz1kb2N1bWVudC5nZXRFbGVtZW50QnlJZCgnbWNPdXQnKTtvLnRleHRDb250ZW50PSdEYW5nIGNoYXkuLi4nO3RyeXtjb25zdCByPWF3YWl0IGZldGNoKCcvb3MvYXBpL211bHRpY2hhbm5lbC9ydW4nLHttZXRob2Q6J1BPU1QnfSk7Y29uc3QgZD1hd2FpdCByLmpzb24oKTtvLnRleHRDb250ZW50PUpTT04uc3RyaW5naWZ5KGQsbnVsbCwyKX1jYXRjaChlKXtvLnRleHRDb250ZW50PSdMb2k6ICcrZS5tZXNzYWdlfX0KYXN5bmMgZnVuY3Rpb24gbWNTdGF0ZSgpe2NvbnN0IG89ZG9jdW1lbnQuZ2V0RWxlbWVudEJ5SWQoJ21jT3V0Jyk7dHJ5e2NvbnN0IHI9YXdhaXQgZmV0Y2goJy9vcy9hcGkvbXVsdGljaGFubmVsL3N0YXRlJyk7Y29uc3QgZD1hd2FpdCByLmpzb24oKTtvLnRleHRDb250ZW50PUpTT04uc3RyaW5naWZ5KGQsbnVsbCwyKX1jYXRjaChlKXtvLnRleHRDb250ZW50PSdMb2k6ICcrZS5tZXNzYWdlfX0K'
fn = base64.b64decode(fn_b64).decode('utf-8')
marker = 'async function channels()'
if 'async function multich()' not in s:
    s = s.replace(marker, fn + marker, 1)
    print('fn added')
else:
    print('fn exists')
old_map = '{dashboard:dash,channels:channels,'
new_map = '{dashboard:dash,multich:multich,channels:channels,'
if old_map in s:
    s = s.replace(old_map, new_map, 1)
    print('renderer registered')
else:
    print('map not found')
io.open(P, 'w', encoding='utf-8').write(s)
print('written', len(s))
