import io, sys
Q = chr(34)
NL = chr(10)
S4 = chr(32) * 4
S8 = chr(32) * 8
p = 'ops/os_publish.py'
text = io.open(p, encoding='utf-8').read()
old_body = NL.join([
 'def load_yt():',
 S4 + 'with open(TOKEN, ' + Q + 'rb' + Q + ') as f:',
 S8 + 'creds = pickle.load(f)',
 S4 + 'return build(' + Q + 'youtube' + Q + ', ' + Q + 'v3' + Q + ', credentials=creds)',
])
insert = NL.join([
 '# Multi-channel support: set active channel to route token + ledger',
 '_ACTIVE_CHANNEL = None',
 '',
 'def set_channel(channel_id):',
 S4 + 'global _ACTIVE_CHANNEL',
 S4 + '_ACTIVE_CHANNEL = channel_id',
 S4 + 'try:',
 S8 + 'from ops import content_freshness as _cf',
 S8 + '_cf.set_channel(channel_id)',
 S4 + 'except Exception:',
 S8 + 'pass',
 S4 + 'return _ACTIVE_CHANNEL',
 '',
 'def active_channel():',
 S4 + 'return _ACTIVE_CHANNEL',
 '',
 'def _resolve_token_path():',
 S4 + 'if _ACTIVE_CHANNEL:',
 S8 + 'try:',
 S8 + S4 + 'from ops import channel_loader as _ch',
 S8 + S4 + 'cfg = _ch.load(_ACTIVE_CHANNEL)',
 S8 + S4 + 'tp = _ch.token_path(cfg)',
 S8 + S4 + 'if tp and os.path.exists(tp):',
 S8 + S8 + 'return Path(tp)',
 S8 + 'except Exception:',
 S8 + S4 + 'pass',
 S4 + 'return TOKEN',
 '',
 'def load_yt():',
 S4 + 'tp = _resolve_token_path()',
 S4 + 'with open(tp, ' + Q + 'rb' + Q + ') as f:',
 S8 + 'creds = pickle.load(f)',
 S4 + 'return build(' + Q + 'youtube' + Q + ', ' + Q + 'v3' + Q + ', credentials=creds)',
])
if old_body not in text:
 print('ANCHOR NOT FOUND')
 sys.exit(1)
text = text.replace(old_body, insert, 1)
io.open(p, 'w', encoding='utf-8').write(text)
print('OK patched bytes', len(text))
