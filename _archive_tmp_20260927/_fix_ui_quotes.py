import ast
p = 'app/ui/index.html'
src = open(p, encoding='utf-8', newline='').read()
Q = chr(34)
SQ = chr(39)

# Fix: x-text="(j.elapsed_sec||0)+"s"" -> x-text='(j.elapsed_sec||0)+"s"'
old1 = Q + '(j.elapsed_sec||0)+' + chr(92) + Q + 's' + chr(92) + Q + Q
new1 = SQ + '(j.elapsed_sec||0)+' + Q + 's' + Q + SQ
print('old1 found:', old1 in src)
src = src.replace(old1, new1, 1)

old2 = Q + '(j.log_tail||[]).slice(-1)[0] || ' + chr(92) + Q + chr(92) + Q + Q
new2 = SQ + '(j.log_tail||[]).slice(-1)[0] || ' + Q + Q + SQ
print('old2 found:', old2 in src)
src = src.replace(old2, new2, 1)

open(p, 'w', encoding='utf-8', newline='').write(src)
# re-scan
bad = [(i+1,l) for i,l in enumerate(src.splitlines()) if l.count(Q) % 2 == 1]
print('remaining bad lines:', len(bad))
for i,l in bad[:5]:
 print(i,'|',l[:150])
