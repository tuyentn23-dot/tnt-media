import glob, os, collections
fs = glob.glob('ops/*.py')
U = chr(95)
prefixes = collections.Counter()
for f in fs:
 name = os.path.basename(f)
 parts = name.split(U)
 if len(parts) >= 2 and parts[1]:
 prefixes[parts[1][:8]] += 1
print('TOTAL', len(fs))
for k, v in prefixes.most_common(30):
 print(v, k)
