import os, shutil
d='E:/OneDrive/Desktop'
os.makedirs('assets', exist_ok=True)
for name in ['youtube_love_vinyl_dynamic_loop.mp4','youtube_love_vinyl_loop.mp4']:
    src=os.path.join(d,name)
    dst='assets/'+name
    if os.path.exists(src) and not os.path.exists(dst):
        shutil.copyfile(src,dst)
    print(name, os.path.getsize(dst) if os.path.exists(dst) else 0)
