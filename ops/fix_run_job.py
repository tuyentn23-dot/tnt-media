# Thay endpoint /api/jobs/{job_id}/run bằng phiên bản truyền đủ config qua --job-json
import sys
NL = chr(10)
TAB = chr(9)
p = 'app/server.py'
lines = open(p, encoding='utf-8').read().split(NL)
start = None
for i, l in enumerate(lines):
	if l.startswith('@app.post(') and 'run' in l and 'jobs' in l:
		start = i
		break
if start is None:
	print('NOT FOUND start')
	sys.exit(1)
# tìm hết hàm (dòng bắt đầu bằng @app. tiếp theo)
end = start + 1
while end < len(lines) and not lines[end].startswith('@app.'):
	end += 1
print('replace lines', start+1, 'to', end)
new = []
new.append('@app.post(' + chr(39) + '/api/jobs/{job_id}/run' + chr(39) + ')')
new.append('def run_job(job_id: str, dry_run: bool = False):')
new.append(TAB + 'import subprocess')
new.append(TAB + 'c = state.connect()')
new.append(TAB + 'row = c.execute(' + chr(39) + 'SELECT id, channel_id, kind, topic, length_override, voice_override, music_mood, count, require_approval FROM jobs WHERE id=?' + chr(39) + ', (job_id,)).fetchone()')
new.append(TAB + 'if not row:')
new.append(TAB + TAB + 'return JSONResponse({k0: False, k1: k2}, status_code=404)'.replace('k0', chr(39)+'ok'+chr(39)).replace('k1', chr(39)+'error'+chr(39)).replace('k2', chr(39)+'job not found'+chr(39)))
new.append(TAB + 'job_dict = {' + chr(39) + 'job_id' + chr(39) + ': row[' + chr(39) + 'id' + chr(39) + '], ' + chr(39) + 'channel_id' + chr(39) + ': row[' + chr(39) + 'channel_id' + chr(39) + '], ' + chr(39) + 'kind' + chr(39) + ': row[' + chr(39) + 'kind' + chr(39) + '], ' + chr(39) + 'topic' + chr(39) + ': row[' + chr(39) + 'topic' + chr(39) + '], ' + chr(39) + 'length_override' + chr(39) + ': row[' + chr(39) + 'length_override' + chr(39) + '], ' + chr(39) + 'voice_override' + chr(39) + ': row[' + chr(39) + 'voice_override' + chr(39) + '], ' + chr(39) + 'music_mood' + chr(39) + ': row[' + chr(39) + 'music_mood' + chr(39) + '], ' + chr(39) + 'count' + chr(39) + ': row[' + chr(39) + 'count' + chr(39) + '], ' + chr(39) + 'require_approval' + chr(39) + ': bool(row[' + chr(39) + 'require_approval' + chr(39) + ']), ' + chr(39) + 'created_by' + chr(39) + ': ' + chr(39) + 'ui' + chr(39) + '}')
new.append(TAB + 'cmd = [sys.executable, ' + chr(39) + '-m' + chr(39) + ', ' + chr(39) + 'pipeline.runner' + chr(39) + ', ' + chr(39) + '--job-json' + chr(39) + ', json.dumps(job_dict, ensure_ascii=False)]')
new.append(TAB + 'if dry_run:')
new.append(TAB + TAB + 'cmd.append(' + chr(39) + '--dry-run' + chr(39) + ')')
new.append(TAB + 'flags = 0')
new.append(TAB + 'for nm in (' + chr(39) + 'CREATE_NEW_PROCESS_GROUP' + chr(39) + ', ' + chr(39) + 'CREATE_NO_WINDOW' + chr(39) + '):')
new.append(TAB + TAB + 'flags = flags | getattr(subprocess, nm, 0)')
new.append(TAB + 'log = os.path.join(ROOT, ' + chr(39) + 'logs' + chr(39) + ', ' + chr(39) + 'runner' + chr(39) + ' + job_id + ' + chr(39) + '.log' + chr(39) + ')')
new.append(TAB + 'os.makedirs(os.path.dirname(log), exist_ok=True)')
new.append(TAB + 'f = open(log, ' + chr(39) + 'w' + chr(39) + ')')
new.append(TAB + 'subprocess.Popen(cmd, stdout=f, stderr=subprocess.STDOUT, creationflags=flags, cwd=ROOT)')
new.append(TAB + 'return {' + chr(39) + 'ok' + chr(39) + ': True, ' + chr(39) + 'job_id' + chr(39) + ': job_id, ' + chr(39) + 'log' + chr(39) + ': log}')
new.append('')
new.append('')
out = lines[:start] + new + lines[end:]
open(p, 'w', encoding='utf-8', newline='').write(NL.join(out))
print('done, new total', len(out))
