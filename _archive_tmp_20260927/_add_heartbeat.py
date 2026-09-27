import ast
NL = chr(10)
TB = chr(9)
TB2 = TB+TB
TB3 = TB2+TB
Q = chr(39)
p = 'pipeline/runner.py'
src = open(p, encoding='utf-8', newline='').read()

helper_lines = []
helper_lines.append('HEARTBEAT = {' + Q + 'stop' + Q + ': None, ' + Q + 'thread' + Q + ': None}')
helper_lines.append('')
helper_lines.append('')
helper_lines.append('def _start_heartbeat(job_id, interval=60):')
helper_lines.append(TB + 'import threading')
helper_lines.append(TB + 'stop = threading.Event()')
helper_lines.append(TB + 'def _beat():')
helper_lines.append(TB2 + 'while not stop.wait(interval):')
helper_lines.append(TB3 + 'try:')
helper_lines.append(TB3 + TB + 'c = state.init()')
helper_lines.append(TB3 + TB + "c.execute('UPDATE jobs SET updated_at=? WHERE id=?', (state.now(), job_id))")
helper_lines.append(TB3 + TB + 'c.commit()')
helper_lines.append(TB3 + 'except Exception:')
helper_lines.append(TB3 + TB + 'pass')
helper_lines.append(TB + 't = threading.Thread(target=_beat, daemon=True)')
helper_lines.append(TB + 't.start()')
helper_lines.append(TB + 'HEARTBEAT[' + Q + 'stop' + Q + '] = stop')
helper_lines.append(TB + 'HEARTBEAT[' + Q + 'thread' + Q + '] = t')
helper_lines.append('')
helper_lines.append('')
helper_lines.append('def _stop_heartbeat():')
helper_lines.append(TB + 'stop = HEARTBEAT.get(' + Q + 'stop' + Q + ')')
helper_lines.append(TB + 'if stop:')
helper_lines.append(TB2 + 'stop.set()')
helper_lines.append(TB + 'HEARTBEAT[' + Q + 'stop' + Q + '] = None')
helper_lines.append(TB + 'HEARTBEAT[' + Q + 'thread' + Q + '] = None')
helper_lines.append('')
helper_lines.append('')
helper = NL.join(helper_lines) + NL

idx = src.find('def run_job(')
assert idx > 0
src = src[:idx] + helper + src[idx:]

log_line = TB + "log('start job: ' + job.job_id + ' channel=' + job.channel_id)" + NL
assert log_line in src
src = src.replace(log_line, log_line + TB + '_start_heartbeat(job.job_id, 60)' + NL, 1)

open(p, 'w', encoding='utf-8', newline='').write(src)
ast.parse(open(p, encoding='utf-8').read())
print('AST OK')
