import os
d='E:/OneDrive/Desktop'
for f in os.listdir(d):
    if f.lower().endswith(('.mp4','.mkv','.webm','.mov')):
        p=os.path.join(d,f)
        print(f.encode('ascii','replace').decode('ascii'), os.path.getsize(p))
