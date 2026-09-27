import ast
NL = chr(10)
TB = chr(9)
p = 'pipeline/runner.py'
src = open(p, encoding='utf-8', newline='').read()

# Add stop calls before every 'return' inside run_job
# Simplest: add stop in main() finally
main_marker = 'def main():'
idx = src.find(main_marker)
assert idx > 0
rest = src[idx:]

# find call to run_job in main
call = "r = run_job(j, dry_run=args.dry_run, item_id=getattr(args, 'item_id', None))"
assert call in rest
rest2 = rest.replace(call, 'try:' + NL + TB + TB + call + NL + TB + 'finally:' + NL + TB + TB + '_stop_heartbeat()', 1)

src = src[:idx] + rest2
open(p, 'w', encoding='utf-8', newline='').write(src)
ast.parse(open(p, encoding='utf-8').read())
print('AST OK')
