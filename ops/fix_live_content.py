p = 'ops/live_content.py'
src = open(p, encoding='utf-8').read()
NL = chr(10)
T = chr(9)
# Tìm và thay thế hàm rss_to_item
start = src.find('def rss_to_item(')
if start < 0:
	print('not found rss_to_item')
	sys.exit(1)
# tìm def tiếp theo
nextdef = src.find(NL + 'def ', start + 10)
if nextdef < 0:
	nextdef = len(src)
new_fn = (
	'def _strip_html(s):' + NL
	+ T + 'import re' + NL
	+ T + 's = re.sub(r' + chr(60) + 'script[^' + chr(62) + ']' + chr(62) + '.?' + chr(60) + '/script' + chr(62) + chr(39) + ', ' + chr(39) + chr(39) + ', s, flags=re.S|re.I)' + NL
	+ T + 's = re.sub(r' + chr(39) + chr(60) + '[^' + chr(62) + ']+' + chr(62) + chr(39) + ', ' + chr(39) + chr(39) + ', s)' + NL
	+ T + 's = re.sub(r' + chr(39) + 'https?://' + chr(92) + 'S+' + chr(39) + ', ' + chr(39) + chr(39) + ', s)' + NL
	+ T + 's = re.sub(r' + chr(39) + chr(92) + 's+' + chr(39) + ', ' + chr(32) + ', s)' + NL
	+ T + 'return s.strip()' + NL + NL + NL
	+ 'def rss_to_item(r, kind, channel):' + NL
	+ T + 'title = strip_html(r.get(' + chr(39) + 'title' + chr(39) + ') or ' + chr(39) + chr(39) + ')' + NL
	+ T + 'body = strip_html(r.get(' + chr(39) + 'body' + chr(39) + ') or ' + chr(39) + chr(39) + ')' + NL
	+ T + 'url = r.get(' + chr(39) + 'url' + chr(39) + ', ' + chr(39) + chr(39) + ')' + NL
	+ T + 'if len(title) < 20:' + NL
	+ T*2 + 'return None' + NL
	+ T + 'vid = ' + chr(39) + 'live' + chr(39) + ' + kind + ' + chr(39) + '' + chr(39) + ' + _slug(title + url)' + NL
	+ T + 'hook = title[:150]' + NL
	+ T + 'b = body[:600] if body else title' + NL
	+ T + 'payoff = title[:80]' + NL
	+ T + 'return {' + chr(39) + 'id' + chr(39) + ': vid, ' + chr(39) + 'topic' + chr(39) + ': kind, ' + chr(39) + 'hook' + chr(39) + ': hook, ' + chr(39) + 'body' + chr(39) + ': b, ' + chr(39) + 'payoff' + chr(39) + ': payoff, ' + chr(39) + 'source_url' + chr(39) + ': url}' + NL + NL + NL
)
out = src[:start] + new_fn + src[nextdef:]
open(p, 'w', encoding='utf-8', newline='').write(out)
print('replaced')
