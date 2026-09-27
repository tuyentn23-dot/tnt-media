p = 'ops/live_content.py'
src = open(p, encoding='utf-8').read()
NL = chr(10)
T = chr(9)
Q = chr(39)
start = src.find('def _strip_html(')
if start < 0:
	start = src.find('def rss_to_item(')
nextdef = src.find(NL + 'def rss_to_item(', start + 5)
if nextdef < 0:
	print('not found rss')
	sys.exit(1)
new_fn = (
	'def _strip_html(s):' + NL
	+ T + 'from html.parser import HTMLParser' + NL
	+ T + 'class P(HTMLParser):' + NL
	+ T2 + 'def ' + chr(95)2 + 'init' + chr(95)2 + '(self):' + NL
	+ T3 + 'super().' + chr(95)2 + 'init' + chr(95)2 + '()' + NL
	+ T3 + 'self.parts = []' + NL
	+ T2 + 'def handle_data(self, d):' + NL
	+ T3 + 'self.parts.append(d)' + NL
	+ T + 'pp = P()' + NL
	+ T + 'try:' + NL
	+ T2 + 'pp.feed(s or ' + Q + Q + ')' + NL
	+ T + 'except Exception:' + NL
	+ T*2 + 'return (s or ' + Q + Q + ').strip()' + NL
	+ T + 'import re' + NL
	+ T + 'txt = ' + Q + ' ' + Q + '.join(pp.parts)' + NL
	+ T + 'txt = re.sub(r' + Q + 'https?:' + chr(92) + chr(92) + '/' + chr(92) + chr(92) + '/' + chr(92) + 'S+' + Q + ', ' + Q + Q + ', txt)' + NL
	+ T + 'txt = re.sub(r' + Q + chr(92) + 's+' + Q + ', ' + Q + ' ' + Q + ', txt)' + NL
	+ T + 'return txt.strip()' + NL + NL + NL
)
out = src[:start] + new_fn + src[nextdef:]
open(p, 'w', encoding='utf-8', newline='').write(out)
print('done')
