import subprocess, os
FF='tools/ffmpeg.exe'
src='assets/song_youaremyonlyone.webm'
dst='assets/song_youaremyonlyone.m4a'
r=subprocess.run([FF,'-y','-i',src,'-c:a','aac','-b:a','192k',dst], capture_output=True, text=True, encoding='utf-8', errors='replace')
print('rc', r.returncode)
print('dst', os.path.exists(dst), os.path.getsize(dst) if os.path.exists(dst) else 0)
# do duration
r2=subprocess.run([FF,'-i',dst], capture_output=True, text=True, encoding='utf-8', errors='replace')
for l in (r2.stderr or '').splitlines():
    if 'Duration' in l:
        print(l.strip().encode('ascii','replace').decode('ascii'))
