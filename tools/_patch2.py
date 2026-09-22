import io, sys
p = 'ops/os_publish.py'
text = io.open(p, encoding='utf-8').read()
NL = chr(10)
old_body = NL.join([
 'def load_yt():',
 ' with open(TOKEN, "rb") as f:',
 ' creds = pickle.load(f)',
 ' return build("youtube