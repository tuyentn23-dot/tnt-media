# Chèn import + include_router vào app/server.py sau dòng 'app = FastAPI(...)'
import sys, os
NL = chr(10)
p = 'app/server.py'
lines = open(p, encoding='utf-8').read().split(NL)
out = []
done = False
for l in lines:
	out.append(l)
	if (not done) and l.startswith('app = FastAPI('):
		out.append('')
		out.append('try:')
		out.append(chr(9) + 'from app._routes_publish import router as _pub_router')
		out.append(chr(9) + 'app.include_router(_pub_router)')
		out.append('except Exception as _e:')
		out.append(chr(9) + 'print(' + chr(34) + '[server] publish router FAIL:' + chr(34) + ', str(_e)[:200])')
		done = True
if not done:
	print('NOT FOUND')
	sys.exit(1)
open(p, 'w', encoding='utf-8', newline='').write(NL.join(out))
print('inserted, lines=', len(out))
