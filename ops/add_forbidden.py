p = 'ops/live_content.py'
src = open(p, encoding='utf-8').read()
NL = chr(10)
T = chr(9)
Q = chr(39)
# thêm forbidden list và filter vào rss_to_item
guard = (
	'FORBIDDEN_KW = [' + Q + 'hiep dam' + Q + ', ' + Q + 'hiếp dâm' + Q + ', ' + Q + 'cuong hiep' + Q + ', ' + Q + 'cưỡng hiếp' + Q + ', ' + Q + 'tu tu' + Q + ', ' + Q + 'tự tử' + Q + ', ' + Q + 'giet nguoi' + Q + ', ' + Q + 'giết người' + Q + ', ' + Q + 'ma tuy' + Q + ', ' + Q + 'ma túy' + Q + ', ' + Q + 'dam nhau' + Q + ', ' + Q + 'đâm nhau' + Q + ', ' + Q + 'cheat' + Q + ']' + NL + NL + NL
	+ 'def _is_forbidden(text):' + NL
	+ T + 'low = (text or ' + Q + Q + ').lower()' + NL
	+ T + 'for k in FORBIDDEN_KW:' + NL
	+ T2 + 'if k.lower() in low:' + NL
	+ T3 + 'return True' + NL
	+ T + 'return False' + NL + NL + NL
)
src = src.replace('def rss_to_item(', guard + 'def rss_to_item(', 1)
# thêm check trong rss_to_item sau khi strip
check = (
	T + 'if _is_forbidden(title) or _is_forbidden(body):' + NL
	+ T*2 + 'return None' + NL
)
marker = T + 'if len(title) < 20:'
src = src.replace(marker, check + marker, 1)
open(p, 'w', encoding='utf-8', newline='').write(src)
print('added forbidden filter')
