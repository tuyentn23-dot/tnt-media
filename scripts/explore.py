import os
for root in ['content','library','projects','output']:
    print('===', root, '===')
    if os.path.isdir(root):
        for dp, dn, fn in os.walk(root):
            lvl = dp.count(os.sep)
            if lvl <= 2:
                print(dp, '->', len(fn), 'files')
    else:
        print('(missing)')
