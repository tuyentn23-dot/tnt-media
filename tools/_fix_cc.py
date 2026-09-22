import io
P='ops/control_center.py'
s=io.open(P,encoding='utf-8').read()
lines=s.split(chr(10))
for i in range(178,190):
    if i < len(lines):
        print(i+1, lines[i].encode('ascii','replace').decode('ascii'))
