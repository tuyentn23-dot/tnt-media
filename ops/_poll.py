import time,os
def rd(p):
    return open(p,encoding='utf-8').read() if os.path.exists(p) else ''
out=''
err=''
for i in range(12):
    time.sleep(5)
    out=rd('ops/_pub1.out')
    err=rd('ops/_pub1.err')
    print('t', (i+1)*5, len(out), len(err))
    if ('DONE' in out) or ('Traceback' in err):
        break
print('==OUT==')
print(out[-1500:])
print('==ERR==')
print(err[-800:])
