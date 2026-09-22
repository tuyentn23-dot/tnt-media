import io, sys
Q = chr(34)
NL = chr(10)
p = 'ops/os_publish.py'
text = io.open(p, encoding='utf-8').read()
old_body = NL.join([
 'def load_yt():',
 ' with open(TOKEN, ' + Q + 'rb' + Q + ') as f:',
 ' creds = pickle.load(f)',
 ' return build(' + Q + 'youtube' + Q + ', ' + Q + 'v3' + Q + ', credentials=creds)',
])
insert = NL.join([
 '# Multi-channel support: set active channel to route token + ledger',
 '_ACTIVE_CHANNEL = None',
 '',
 'def set_channel(channel_id):',
 ' global _ACTIVE_CHANNEL',
 ' _ACTIVE_CHANNEL = channel_id',
 ' try:',
 ' from ops import content_freshness as _cf',
 ' _cf.set_channel(channel_id)',
 ' except Exception:',
 ' pass',
 ' return _ACTIVE_CHANNEL',
 '',
 'def active_channel():',
 ' return _ACTIVE_CHANNEL',
 '',
 'def _resolve_token_path():',
 ' if _ACTIVE_CHANNEL:',
 ' try:',
 ' from ops import channel_loader as _ch',
 ' cfg = _ch.load(_ACTIVE_CHANNEL)',
 ' tp = _ch.token_path(cfg)',
 ' if tp and os.path.exists(tp):',
 ' return Path(tp)',
 ' except Exception:',
 ' pass',
 ' return TOKEN',
 '',
 'def load_yt():',
 ' tp = _resolve_token_path()',
 ' with open(tp, ' + Q + 'rb' + Q + ') as f:',
 ' creds = pickle.load(f)',
 ' return build(' + Q + 'youtube' + Q + ', ' + Q + 'v3' + Q + ', credentials=creds)',
])
if old_body not in text:
 print('ANCHOR NOT FOUND')
 sys.exit(1)
text = text.replace(old_body, insert, 1)
io.open(p, 'w', encoding='utf-8').write(text)
print('OK patched bytes', len(text))
