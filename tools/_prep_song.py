import os, shutil
src='E:/OneDrive/Desktop/L\u1eb7ng Im Th\u01b0\u01a1ng Anh 1.mp4'
# fallback: quet ten
if not os.path.exists(src):
    d='E:/OneDrive/Desktop'
    for f in os.listdir(d):
        if 'ng Im Th' in f and f.endswith('.mp4'):
            src=os.path.join(d,f); break
print('src found:', os.path.exists(src))
dst='D:/TNT_AI/venture_foundry/media/assets/song_lang_im_thuong_anh.mp4'
os.makedirs(os.path.dirname(dst), exist_ok=True)
if os.path.exists(src) and not os.path.exists(dst):
    shutil.copyfile(src, dst)
print('dst size:', os.path.getsize(dst) if os.path.exists(dst) else 0)
