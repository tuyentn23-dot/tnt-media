import base64,sys
p=sys.argv[1]
d=base64.b64decode(sys.stdin.read())
open(p,'wb').write(d)
print('WROTE',p,len(d))
