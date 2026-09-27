import os, sys, tempfile, sqlite3
ROOT = os.path.dirname(os.path.dirname(os.path.abspath('file')))
sys.path.insert(0, ROOT)
os.chdir(ROOT)

from pipeline import scheduler as sch
from ops import backup_state as bs

PASS = [0]
FAIL = [0]

def check(name, cond):
    if cond:
        PASS[0] += 1
        print('[PASS]', name)
    else:
        FAIL[0] += 1
        print('[FAIL]', name)


def test_parse_cron():
    r = sch.parse_cron('0 9 * * 1-5')
    check('parse 0 9 * * 1-5', bool(r) and r['minute'] == {0} and r['hour'] == {9})
    check('weekday 1-5', bool(r) and r['weekday'] == {1,2,3,4,5})
    r2 = sch.parse_cron('*/5 * * * *')
    check('/5 minute', bool(r2) and r2['minute'] == set(range(0,60,5)))
    check('invalid cron', sch.parse_cron('bad') is None)


def test_backup():
    tmpd = tempfile.mkdtemp(prefix='bk_test_')
    dbp = os.path.join(tmpd, 'src.db')
    c = sqlite3.connect(dbp)
    c.execute('CREATE TABLE t (id INTEGER)')
    c.execute('INSERT INTO t VALUES (1),(2),(3)')
    c.commit(); c.close()
    dst = bs.backup_sqlite(dbp, tmpd)
    check('backup file exists', os.path.exists(dst))
    tables = bs.verify(dst)
    check('backup has table t', 't' in tables)
    check('backup t has 3 rows', tables.get('t', 0) == 3)


test_parse_cron()
test_backup()
print()
print('SUMMARY:', PASS[0], '/', FAIL[0])
sys.exit(0 if FAIL[0] == 0 else 1)
