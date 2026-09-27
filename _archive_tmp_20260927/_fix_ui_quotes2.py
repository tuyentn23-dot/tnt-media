import ast
p = 'app/ui/index.html'
lines = open(p, encoding='utf-8', newline='').read().splitlines(keepends=True)
Q = chr(34)
SQ = chr(39)
NL = chr(10)

# Fix line 95 (index 94)
old95 = '			<td class=' + Q + 'text-xs text-gray-600' + Q + ' x-text=' + Q + '(j.elapsed_sec||0)+' + chr(92) + Q + 's' + chr(92) + Q + Q + '></td>'
new95 = '			<td class=' + Q + 'text-xs text-gray-600' + Q + ' x-text=' + SQ + '(j.elapsed_sec||0)+' + Q + 's' + Q + SQ + '></td>'
print('old95 in lines:', lines[94].rstrip(NL) == old95)
if lines[94].rstrip(NL) == old95:
 lines[94] = new95 + NL

# Fix line 96 (index 95)
old96 = '			<td class=' + Q + 'text-xs text-gray-500 max-w-xs truncate' + Q + ' :title=' + Q + 'JSON.stringify(j.log_tail)' + Q + ' x-text=' + Q + '(j.log_tail||[]).slice(-1)[0] || ' + chr(92) + Q + chr(92) + Q + Q + '></td>'
new96 = '			<td class=' + Q + 'text-xs text-gray-500 max-w-xs truncate' + Q + ' :title=' + Q + 'JSON.stringify(j.log_tail)' + Q + ' x-text=' + SQ + '(j.log_tail||[]).slice(-1)[0] || ' + Q + Q + SQ + '></td>'
print('old96 in lines:', lines[95].rstrip(NL) == old96)
if lines[95].rstrip(NL) == old96:
 lines[95] = new96 + NL

open(p, 'w', encoding='utf-8', newline='').write(''.join(lines))
print('written')
