# optimal_times.py - Phan tich gio vang dang bai
import os, json, sqlite3

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB = os.path.join(ROOT, 'system', 'state.db')

def best_hours(top=3):
 con = sqlite3.connect(DB)
 rows = list(con.execute('SELECT publishedAt FROM publishes'))
 con.close()
 hours = [int(r[0][11:13]) for r in rows if r[0] and len(r[0]) >= 13]
 counts = [(h, hours.count(h)) for h in set(hours)]
 counts.sort(key=lambda x: x[1], reverse=True)
 return counts[:top]

if __name__ == '__main__':
 print(best_hours())
