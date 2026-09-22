src = open('tools/_mia_src.txt', encoding='utf-8').read()
open('ops/mia_content.py', 'w', encoding='utf-8').write(src)
print('moved OK')
