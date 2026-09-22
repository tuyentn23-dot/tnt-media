import os
def show(d):
    print('=== ', d)
    if not os.path.isdir(d):
        print('NO DIR')
        return
    for f in sorted(os.listdir(d))[:40]:
        p=os.path.join(d,f)
        sz=os.path.getsize(p) if os.path.isfile(p) else 'DIR'
        print(sz, f)
show('music_bank')
show('assets/music')
show('assets/music_clips')
