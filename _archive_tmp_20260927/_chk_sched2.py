lines = open('pipeline/scheduler.py', encoding='utf-8').read().splitlines()
for i in range(105, 120):
 print(i + 1, repr(lines[i]))
