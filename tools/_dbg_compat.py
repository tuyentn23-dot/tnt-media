import os, sys
sys.path.insert(0, os.getcwd())
os.environ['IMAGEIO_FFMPEG_EXE'] = os.path.abspath('tools/ffmpeg.exe')
import ops.compat as m
e = getattr(m, chr(95) + 'editor')
cn = getattr(e, chr(95) + chr(95) + 'code' + chr(95) + chr(95))
print('co_consts:', cn.co_consts[:6])
print('co_names:', cn.co_names[:10])
