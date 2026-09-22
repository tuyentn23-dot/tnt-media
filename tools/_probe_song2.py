import subprocess
v='assets/song_youaremyonlyone.webm'
r=subprocess.run(['tools/ffmpeg.exe','-i',v], capture_output=True, text=True, encoding='utf-8', errors='replace')
for l in (r.stderr or '').splitlines():
    if 'Duration' in l or 'Stream' in l or 'Input' in l:
        print(l.strip().encode('ascii','replace').decode('ascii'))
print('---head---')
print(open(v,'rb').read(16))
