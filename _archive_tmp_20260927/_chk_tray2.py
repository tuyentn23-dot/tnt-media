lines = open('app/tray.py', encoding='utf-8').read().splitlines()
for i in range(190, 200):
 print('L' + str(i+1) + ':', lines[i])
