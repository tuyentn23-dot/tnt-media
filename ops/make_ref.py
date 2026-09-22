import os
files = ["channels.md", "tools.md", "workflow.md", "wrapper_rules.md", "lessons.md"]
parts = []
for f in files:
 p = os.path.join("docs", f)
 if os.path.exists(p):
 parts.append(open(p, encoding="utf-8").read())
combined = (chr(10) + chr(10) + chr(61) * 60 + chr(10) + chr(10)).join(parts)
open("REFERENCE.md", "w", encoding="utf-8").write(combined)
print("REFERENCE.md: ", len(combined))