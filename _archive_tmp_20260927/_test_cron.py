import os, sys
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)
os.chdir(ROOT)
from pipeline import scheduler as s
STAR = s.STARMARK
print('5step:', sorted(s._expand_cron_field(STAR + chr(47) + '5', 0, 59)))
cron = '0 9 ' + STAR + ' ' + STAR + ' 1-5'
print('cron:', cron)
print('parse:', s.parse_cron(cron))
print('parse 0 9 1 1 0:', s.parse_cron('0 9 1 1 0'))
