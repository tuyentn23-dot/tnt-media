# ops/start.py - LENH DUY NHAT KHI VAO PHIEN MOI
# Chay: python ops/start.py
import os, sys, sqlite3, re
sys.stdout.reconfigure(encoding='utf-8')
ROOT = os.getcwd()
LINE = '=' * 60

def show(path, title):
	print(LINE)
	print('### ' + title + ' (' + path + ')')
	print(LINE)
	if not os.path.exists(path):
		print('(khong co file)')
		return
	txt = open(path, encoding='utf-8').read()
	print(txt)

print(LINE)
print('TNT MEDIA OS - NAP NGU CANH PHIEN MOI')
print(LINE)
show('BRAIN.md', 'BO NAO - DOC KY')
print()
show('STATE.md', 'TRANG THAI')
print()

print(LINE)
print('### DB VAN HANH (state/pipeline.db)')
print(LINE)
db = os.path.join(ROOT, 'state', 'pipeline.db')
c = sqlite3.connect(db)
print('-- KENH --')
for r in c.execute('SELECT id, enabled, kinds FROM channels ORDER BY id'):
	print(' ' + str(r[0]) + ' | enabled=' + str(r[1]) + ' | ' + str(r[2]))
print('-- JOBS --')
for r in c.execute('SELECT status, COUNT() FROM jobs GROUP BY status'):
	print(' ' + str(r[0]) + ': ' + str(r[1]))
print('-- PUBLICATIONS --')
n = c.execute('SELECT COUNT() FROM publications').fetchone()[0]
print(' total: ' + str(n))
print(' gan nhat:')
for r in c.execute('SELECT channel_id, youtube_url, created_at FROM publications ORDER BY created_at DESC LIMIT 10'):
	print(' ' + str(r[0]) + ' | ' + str(r[1]) + ' | ' + str(r[2]))

print()
print(LINE)
print('### VIEC CON LAI')
print(LINE)
brain = open('BRAIN.md', encoding='utf-8').read()
m = re.search(r'## 9\. VIEC CON LAI.*?(?=## 10\.)', brain, re.S)
print(m.group(0).strip() if m else '(khong tim thay)')

print()
print(LINE)
print('SAN SANG. Chon 1-3 viec, lam, roi chay python ops/end.py khi ket thuc.')
print(LINE)
