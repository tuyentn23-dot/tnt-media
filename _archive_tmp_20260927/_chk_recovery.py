lines = open('pipeline/recovery.py', encoding='utf-8').read().splitlines()
for i, l in enumerate(lines):
 print(i+1, '|', l)
