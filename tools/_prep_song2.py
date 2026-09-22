import os, shutil
# 1) copy anh bia 3.png
src_png = 'E:/OneDrive/Pictures/Vi/3.png'
dst_png = 'D:/TNT_AI/venture_foundry/media/assets/youaremyonlyone_cover.png'
os.makedirs(os.path.dirname(dst_png), exist_ok=True)
print('png exists:', os.path.exists(src_png))
if os.path.exists(src_png):
    shutil.copyfile(src_png, dst_png)
    print('png size:', os.path.getsize(dst_png))
# 2) copy webm nhac
src_webm = None
d='E:/OneDrive/Pictures/Vi'
for f in os.listdir(d):
    if 'only one' in f.lower() and f.lower().endswith('.webm'):
        src_webm = os.path.join(d,f); break
print('webm found:', src_webm)
dst_webm = 'D:/TNT_AI/venture_foundry/media/assets/song_youaremyonlyone.webm'
if src_webm and os.path.exists(src_webm):
    shutil.copyfile(src_webm, dst_webm)
    print('webm size:', os.path.getsize(dst_webm))
print('png from PIL:', end=' ')
try:
    from PIL import Image
    im = Image.open(dst_png)
    print(im.size, im.mode)
except Exception as e:
    print('ERR', e)
