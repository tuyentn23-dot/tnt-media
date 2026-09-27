import sys
SP = chr(32)
lines = open('ops/ffmpeg_render.py', encoding='utf-8').read().splitlines()
for i, l in enumerate(lines):
 SP4 = SP+SP+SP+SP
 if '_work' in l:
 print(i + 1, '|', repr(l))
