import os
results = []
for root, _, files in os.walk('.'):
 if 'backup' in root:
 results.append(root)
print(results)
