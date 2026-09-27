import sys, time
sys.path.insert(0, '.')
from pipeline import scheduler

for hh in ['08:00', '09:00', '12:00', '15:00', '21:00']:
	t = time.strptime(hh, '%H:%M')
	print(hh, 'Mia:', scheduler.due_now('0 9,15,21 * * *', t), 'vilevi:', scheduler.due_now('0 8,12,18,21 * * *', t))
