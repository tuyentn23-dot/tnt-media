import re
path = r'C:\Users\DELL\Desktop\TNT Media.lnk'
with open(path, 'rb') as f:
	data = f.read()
print('size', len(data))
ascii_ = re.findall(rb'[\x20-\x7e]{4}', data)
uni = re.findall(rb'(?:[\x20-\x7e]\x00){4}', data)
print('--- ascii ---')
for s in ascii_:
	print(s.decode('ascii', 'ignore'))
print('--- unicode ---')
for s in uni:
	print(s.decode('utf-16-le', 'ignore'))
