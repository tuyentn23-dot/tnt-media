p = 'ops/channel_loader.py'
src = open(p, encoding='utf-8').read()
NL = chr(10)
T = chr(9)
T2 = T + T
Q = chr(39)
old = T2 + 'print(' + Q + '[loader] live err:' + Q + ', str(e)[:80])' + NL + T + 'return items'
new = (T2 + 'print(' + Q + '[loader] live err:' + Q + ', str(e)[:80])' + NL
	+ T + 'try:' + NL
	+ T2 + 'from ops import live_content as _lc2' + NL
	+ T2 + 'items = _lc2.filter_items(items)' + NL
	+ T + 'except Exception:' + NL
	+ T2 + 'pass' + NL
	+ T + 'return items')
if old not in src:
	print('pattern not found')
else:
	src = src.replace(old, new, 1)
	open(p, 'w', encoding='utf-8', newline='').write(src)
	print('wired filter')
