# -*- coding: utf-8 -*-
import io
P = 'ops/os_publish.py'
s = io.open(P, encoding='utf-8').read()
mark = 'def publish(video_path, title, description='
i = s.find(mark)
print('publish at', i)
# insert a health check right after the docstring line inside publish
doc_end = s.find('"""', s.find('"""', i) + 3) + 3
health = (
 "\n    # HEALTH CHECK: chan video den/loi truoc khi upload (khong the bo qua bang force)\n"
 "    try:\n"
 "        from ops import video_health as _vh\n"
 "        _h = _vh.check(str(video_path))\n"
 "        if not _h.get('ok'):\n"
 "            return {'ok': False, 'blocked': True, 'reason': 'video-health', 'health': _h}\n"
 "    except Exception as _he:\n"
 "        pass\n"
)
s2 = s[:doc_end] + health + s[doc_end:]
io.open(P, 'w', encoding='utf-8').write(s2)
import ast
ast.parse(s2)
print('patched + syntax OK, new len', len(s2))
