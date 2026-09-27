import os, sys, sqlite3
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(FILEMARK)))
os.chdir(ROOT)
c = sqlite3.connect('state/pipeline.db')
c.row_factory = sqlite3.Row
rows = c.execute('SELECT status, COUNT(1) AS n FROM publications GROUP BY status').fetchall()
print('PUBLICATIONS BY STATUS:')
for r in rows:
 print(' ', r['status'], '=', r['n'])
jrows = c.execute('SELECT status, COUNT(1) AS n FROM jobs GROUP BY status').fetchall()
print('JOBS BY STATUS:')
for r in jrows:
 print(' ', r['status'], '=', r['n'])
