fn = 'ops/build_gacha_viral.py'
raw = open(fn, 'rb').read()
# Tim start PARTS va end ]
start = raw.find(b'PARTS = [')
end = raw.find(b']', start)
print('start:', start, 'end:', end)
# New PARTS: 5 cau ngan hon (~50 ky tu)
P = ['POV: Cô gái mèo hồng dễ thương nhất trường!', 'Ai cũng ngưỡng mộ ngoại hình của cô ấy!', 'Nhưng không ai biết bí mật đằng sau!', 'Cô ấy khóc một mình mỗi đêm!', 'Và rồi cô ấy quyết định yêu bản thân!']
lines = []
lines.append(b'PARTS = [')
for p in P:
	lines.append(b'' + chr(9) + b'' + repr(p).encode('utf-8') + b',')
lines.append(b']')
new_block = b''.join(lines)
new_raw = raw[:start] + new_block + raw[end+1:]
open(fn, 'wb').write(new_raw)
print('done, new size:', len(new_raw))