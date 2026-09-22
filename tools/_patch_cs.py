# -- coding: utf-8 --
import io
P = 'ops/channel_style.py'
s = io.open(P, encoding='utf-8').read()
T = chr(9)
NL = chr(10)
old = T + 'cs = []' + NL + T + 'if seed is None:'
block = [
 T + 'cs = []',
 T + '_topic = str(item.get("topic