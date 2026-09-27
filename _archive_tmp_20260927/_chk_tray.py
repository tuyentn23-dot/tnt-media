lines = open('app/tray.py', encoding='utf-8').read().splitlines()
for i in range(180, 205):
 print(i+1, '|', lines[i])
