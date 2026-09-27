import ast
NL = chr(10)
p = 'pipeline/scheduler.py'
src = open(p, encoding='utf-8').read()

# Cron weekday: 0=Sun, 1=Mon..6=Sat. Python tm_wday: 0=Mon..6=Sun
# Convert cron weekday to tm_wday: cron 0(Sun)->6, cron 1..6(Mon..Sat)->0..5
old_due = (
 "	if now.tm_wday not in parsed['weekday']:" + NL
 + '		return False' + NL
)
new_due = (
 "	cron_to_tm = {0: 6, 1: 0, 2: 1, 3: 2, 4: 3, 5: 4, 6: 5}" + NL
 + "	allowed_tm = {cron_to_tm[c] for c in parsed['weekday']}" + NL
 + "	if now.tm_wday not in allowed_tm:" + NL
 + '		return False' + NL
)

print('old in src:', old_due in src)
if old_due in src:
 src = src.replace(old_due, new_due, 1)
 open(p, 'w', encoding='utf-8', newline='').write(src)
 print('PATCHED weekday mapping')
else:
 print('NOT FOUND')
ast.parse(open(p, encoding='utf-8').read())
print('AST OK')
