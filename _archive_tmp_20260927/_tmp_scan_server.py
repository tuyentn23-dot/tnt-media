import sys
p='app/server.py'
lines=open(p,encoding='utf-8').read().splitlines()
start=int(sys.argv[1]) if len(sys.argv)>1 else 90
end=int(sys.argv[2]) if len(sys.argv)>2 else 200
for i in range(start-1,min(end,len(lines))):
 sys.stdout.write(str(i+1)+chr(9)+lines[i]+chr(10))
