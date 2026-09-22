# -*- coding: utf-8 -*-
import io
P = 'ops/os_publish.py'
s = io.open(P, encoding='utf-8').read()
# Chen set thumbnail sau khi upload thanh cong (sau dong vid = resp.get)
mark = 'vid = resp.get(' + chr(34) + 'id' + chr(34) + ')'
i = s.find(mark)
print('found vid line at', i)
if i >= 0:
    end = s.find(chr(10), i) + 1
    block = (
        '\n    # Tu dong tao + set thumbnail\n'
        '    try:\n'
        '        from ops.thumbnail_generator import generate_high_ctr_thumbnail\n'
        '        _thumb = str(p).replace(".mp4", "_thumb.jpg")\n'
        '        generate_high_ctr_thumbnail(title[:60], output_path=_thumb)\n'
        '        if os.path.exists(_thumb) and vid:\n'
        '            yt.thumbnails().set(videoId=vid, media_body=MediaFileUpload(_thumb)).execute()\n'
        '    except Exception as _te:\n'
        '        pass\n'
    )
    s2 = s[:end] + block + s[end:]
    io.open(P, 'w', encoding='utf-8').write(s2)
    import ast
    ast.parse(s2)
    print('patched thumbnail + syntax OK')
else:
    print('MARK NOT FOUND')
