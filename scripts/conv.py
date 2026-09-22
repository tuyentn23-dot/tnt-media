p='scripts/get_all.py'
s=open(p,encoding='utf-8').read()
out=[]
for ln in s.split(chr(10)):
	if ln.strip() == '':
		out.append(ln)
		continue
	st=ln.lstrip(chr(32))
	lead=len(ln)-len(st)
	if lead > 0:
		out.append(chr(9) * (lead // 4) + st)
	else:
		out.append(ln)
open(p, 'w', encoding='utf-8').write(chr(10).join(out))
print('converted')
