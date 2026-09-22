fn = 'ops/build_gacha_viral.py'
raw = open(fn, 'rb').read()
start = raw.find(b'PARTS = [')
end = raw.find(b']', start)
P = [
	'POV: Cô gái mèo hồng dễ thương nhất trường!',
	'Ai cũng ngưỡng mộ ngoại hình của cô ấy!',
	'Nhưng không ai biết bí mật đằng sau!',
	'Cô ấy khóc một mình mỗi đêm!',
	'Và rồi cô ấy quyết định yêu bản thân!'
]
TAB = bytes([9])
parts_bytes = [b'PARTS = [']
for p in P:
	line = TAB + p.encode('utf-8') + b','
	parts_bytes.append(line)
parts_bytes.append(b']')
new_block = bytes([10]).join(parts_bytes)
new_raw = raw[:start] + new_block + raw[end+1:]
open(fn, 'wb').write(new_raw)
print('done:', len(new_raw))