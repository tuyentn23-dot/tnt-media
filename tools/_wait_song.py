import os, time
p='output/vile_lang_im_thuong_anh.mp4'
last=-1
for i in range(20):
    time.sleep(6)
    if not os.path.exists(p):
        print('waiting...'); continue
    sz=os.path.getsize(p)
    if sz==last and sz>1000000:
        print('done size', sz); break
    last=sz
    print('size', sz)
