import io, sys
p = 'ops/os_publish.py'
text = io.open(p, encoding='utf-8').read()

old_body = (
 'def load_yt():
'
 ' with open(TOKEN, "rb") as f:
'
 ' creds = pickle.load(f)
'
 ' return build("youtube