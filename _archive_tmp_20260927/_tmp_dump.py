import sys
p=sys.argv[1]
start=int(sys.argv[2]) if len(sys.argv)>2 else 1
end=int(sys.argv[3]) if len(sys.argv)>3 else 10**9
lines=open(p,encoding='utf-8',errors='replace').read().splitlines()
for i in range(start-1,min(end,len(lines))):
 sys.stdout.write(str(i+1)+chr(9)+lines[i]+chr(10))
print('TOTAL',len(lines))
