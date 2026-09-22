import os
d='E:/OneDrive/Desktop'
print('dir exists:', os.path.isdir(d))
if os.path.isdir(d):
    for f in os.listdir(d):
        if f.lower().endswith(('.mp4','.mkv','.webm','.mov')) and ('lang' in f.lower() or 'thuong' in f.lower() or 'thương' in f.lower() or 'im' in f.lower()):
            p=os.path.join(d,f)
            print(repr(f), os.path.getsize(p))
