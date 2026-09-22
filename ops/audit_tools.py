import os, json
from datetime import datetime
ROOT = os.getcwd()
OPS = os.path.join(ROOT, 'ops')
linesOf = lambda p: sum(1 for x in open(p, encoding='utf-8', errors='ignore'))
rows = [{'name': n, 'size': os.path.getsize(os.path.join(OPS, n)), 'lines': linesOf(os.path.join(OPS, n)), 'mtime': datetime.fromtimestamp(os.path.getmtime(os.path.join(OPS, n))).isoformat(timespec='seconds')} for n in sorted(os.listdir(OPS)) if n.endswith('.py')]
open(os.path.join(ROOT, 'audit_report.json'), 'w', encoding='utf-8').write(json.dumps({'count': len(rows), 'tools': rows}, indent=2))
print('scanned', len(rows), 'py files')
sizes = sorted([r['size'] for r in rows])
print('size min/median/max:', sizes[0], sizes[len(sizes)//2], sizes[-1])
print('report: audit_report.json')
