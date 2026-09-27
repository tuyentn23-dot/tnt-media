import base64, ast
p = 'app/ui/index.html'
lines = open(p, encoding='utf-8', newline='').read().splitlines(keepends=True)
NL = chr(10)

# Decode exact line 95
b95 = 'CQkJPHRkIGNsYXNzPSJ0ZXh0LXhzIHRleHQtZ3JheS02MDAiIHgtdGV4dD0iKGouZWxhcHNlZF9zZWN8fDApKyJzIiI+PC90ZD4='
old95 = base64.b64decode(b95).decode()
print('old95 repr:', repr(old95))

Q = chr(34)
SQ = chr(39)
new95 = '			<td class=' + Q + 'text-xs text-gray-600' + Q + ' x-text=' + SQ + '(j.elapsed_sec||0)+' + Q + 's' + Q + SQ + '></td>'
print('new95 repr:', repr(new95))
print('match 95:', lines[94].rstrip(NL) == old95, 'match 95+NL:', lines[94] == old95 + NL)
if lines[94].rstrip(NL) == old95:
 lines[94] = new95 + NL

b96 = 'CQkJPHRkIGNsYXNzPSJ0ZXh0LXhzIHRleHQtZ3JheS01MDAgbWF4LXcteHMgdHJ1bmNhdGUiIDp0aXRsZT0iSlNPTi5zdHJpbmdpZnkoai5sb2dfdGFpbCkiIHgtdGV4dD0iKGoubG9nX3RhaWx8fFtdKS5zbGljZSgtMSlbMF0gfHwgIiIiPjwvdGQ+'
old96 = base64.b64decode(b96).decode()
new96 = '			<td class=' + Q + 'text-xs text-gray-500 max-w-xs truncate' + Q + ' :title=' + Q + 'JSON.stringify(j.log_tail)' + Q + ' x-text=' + SQ + '(j.log_tail||[]).slice(-1)[0] || ' + Q + Q + SQ + '></td>'
print('match 96:', lines[95].rstrip(NL) == old96)
if lines[95].rstrip(NL) == old96:
 lines[95] = new96 + NL

open(p, 'w', encoding='utf-8', newline='').write(''.join(lines))
print('written')
print('AFTER 95:', repr(open(p,encoding='utf-8').read().splitlines()[94]))
print('AFTER 96:', repr(open(p,encoding='utf-8').read().splitlines()[95]))
