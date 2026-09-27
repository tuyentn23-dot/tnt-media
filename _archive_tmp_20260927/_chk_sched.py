lines = open('pipeline/scheduler.py', encoding='utf-8').read().splitlines()
print('TOTAL', len(lines))
for i in range(100, len(lines)):
 print(i + 1, repr(lines[i]))
