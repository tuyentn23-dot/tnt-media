import os,sys
sys.path.insert(0,os.getcwd())
import ops.compat
try:
    import moviepy.editor as me
    print('editor import OK')
    for cn in ['VideoFileClip','ImageClip','CompositeVideoClip','AudioFileClip']:
        c=getattr(me,cn,None)
        print(cn, c is not None, hasattr(c,'with_position') if c else None)
except Exception as e:
    print('editor ERR', repr(e)[:200])
