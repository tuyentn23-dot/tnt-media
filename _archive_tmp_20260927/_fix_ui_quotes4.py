import base64
p = 'app/ui/index.html'
src = open(p, encoding='utf-8', newline='').read()
CR = chr(13)
Q = chr(34)
SQ = chr(39)

# Target: x-text="(j.elapsed_sec||0)+"s"" (4 quotes)
old95 = Q + '(j.elapsed_sec||0)+' + Q + 's' + Q + Q
new95 = Q + '(j.elapsed_sec||0)+' + SQ + 's' + SQ + Q
print('old95 found:', old95 in src)
src = src.replace(old95, new95, 1)

old96 = Q + '(j.log_tail||[]).slice(-1)[0] || ' + Q + Q + Q
new96 = Q + '(j.log_tail||[]).slice(-1)[0] || ' + SQ + SQ + Q
print('old96 found:', old96 in src)
src = src.replace(old96, new96, 1)

open(p, 'w', encoding='utf-8', newline='').write(src)
lines = open(p, encoding='utf-8', newline='').read().split(CR + chr(10)) if CR in src else src.split(chr(10))
print('AFTER 95:', repr(lines[94][:120]))
print('AFTER 96:', repr(lines[95][:200]))
