# -- coding: utf-8 --
import os, subprocess, shutil, random, re
try:
	import ops._no_window as _nw
except Exception:
	pass
W, H, FPS = 1080, 1920, 30
def _has_audio(path):
    r = subprocess.run([_ff(), '-i', path, '-hide_banner'], capture_output=True, text=True)
    return 'Audio:' in r.stderr

def _ff():
    root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    ff = os.path.join(root, 'tools', 'ffmpeg.exe')
    return ff if os.path.exists(ff) else 'ffmpeg'
def _dur(path):
    r = subprocess.run([_ff(), '-i', path, '-hide_banner'], capture_output=True, text=True)
    m = re.search('Duration: ([0-9]+):([0-9]+):([0-9.]+)', r.stderr)
    if not m:
        return 0.0
    return int(m.group(1))*3600 + int(m.group(2))*60 + float(m.group(3))
def pick(folder, n=6):
    d = os.path.join('library', folder)
    if not os.path.isdir(d):
        return []
    fs = [os.path.join(d, f) for f in os.listdir(d) if f.lower().endswith('.mp4')]
    random.shuffle(fs)
    return fs[:n]

def _seg(src, out, take, idx):
    z = 1.10 if idx % 2 == 0 else 1.18
    vfc = 'scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,setsar=1,zoompan=z=1+on/500:d=1:s=1080x1920:fps=30'
    cmd = [_ff(), '-y', '-i', src, '-t', str(take), '-vf', vfc, '-an', '-c:v', 'libx264', '-preset', 'veryfast', out]
    subprocess.run(cmd, capture_output=True)
    return os.path.exists(out) and os.path.getsize(out) > 2000


def _seg_169(src, out, take, idx):
 vfc = 'scale=1920:1080:force_original_aspect_ratio=increase,crop=1920:1080,setsar=1,zoompan=z=1+on/500:d=1:s=1920x1080:fps=30'
 cmd = [_ff(), '-y', '-i', src, '-t', str(take), '-vf', vfc, '-an', '-c:v', 'libx264', '-preset', 'veryfast', '-pix_fmt', 'yuv420p', out]
 subprocess.run(cmd, capture_output=True)
 return os.path.exists(out) and os.path.getsize(out) > 2000

TRANSITIONS = ['fade', 'slideleft', 'slideright', 'wipeleft', 'wiperight', 'circleopen', 'circleclose', 'smoothleft', 'smoothright']

def _xfade_join(segs, out, xd=0.4, trans=None):
    import random as _r
    if len(segs) == 1:
        shutil.copy(segs[0], out)
        return True
    inputs = []
    for s in segs:
        inputs += ['-i', s]
    filt = []
    prev = '0:v'
    off = 0.0
    for i in range(1, len(segs)):
        off += (2.0 - xd)
        lbl = 'v' + str(i)
        t = trans or _r.choice(TRANSITIONS)
        filt.append('[' + prev + '][' + str(i) + ':v]xfade=transition=' + t + ':duration=' + str(xd) + ':offset=' + str(off) + '[' + lbl + ']')
        prev = lbl
    fc = ';'.join(filt)
    cmd = [_ff(), '-y'] + inputs + ['-filter_complex', fc, '-map', '[' + prev + ']', '-c:v', 'libx264', '-preset', 'veryfast', out]
    subprocess.run(cmd, capture_output=True, text=True)
    return os.path.exists(out) and os.path.getsize(out) > 5000

def add_music(path, music=None):
    import glob as _g
    ff = _ff()
    if music and os.path.exists(music):
        mp = music
    else:
        beds = _g.glob(os.path.join('music_bank', '*.wav'))
        import random as _r
        mp = _r.choice(beds) if beds else (os.path.join('library', 'music_bed.wav') if os.path.exists(os.path.join('library', 'music_bed.wav')) else None)
    if not mp or not os.path.exists(mp):
        return False
    tmp = path + '.mus.mp4'
    if _has_audio(path):
        fc = '[0:a]volume=1.0[vo];[1:a]volume=0.15[bg];[vo][bg]amix=inputs=2:duration=first:dropout_transition=0[aout]'
        cmd = [ff, '-y', '-i', path, '-stream_loop', '-1', '-i', mp, '-filter_complex', fc, '-map', '0:v', '-map', '[aout]', '-c:v', 'copy', '-c:a', 'aac', '-shortest', tmp]
    else:
        cmd = [ff, '-y', '-i', path, '-stream_loop', '-1', '-i', mp, '-map', '0:v', '-map', '1:a', '-c:v', 'copy', '-c:a', 'aac', '-shortest', tmp]
    r = subprocess.run(cmd, capture_output=True)
    if r.returncode == 0 and os.path.exists(tmp):
        shutil.move(tmp, path)
        return True
    return False
def build(folder, out, voice_text=None, hook=None, caps=None, theme=None, n=6, seg=2.0, music=None, aspect='9:16'):
    from ops import vids_post as vp
    src = pick(folder, n)
    if len(src) < 2:
        return {'ok': False, 'err': 'no footage'}
    tdir = os.path.join(os.path.dirname(out) or '.', '_edit_tmp')
    shutil.rmtree(tdir, ignore_errors=True)
    os.makedirs(tdir, exist_ok=True)
    segs = []
    for i, f in enumerate(src):
        sp = os.path.join(tdir, str(i) + '.mp4')
        seg_fn = _seg_169 if aspect == '16:9' else _seg
        if seg_fn(f, sp, seg, i):
            segs.append(sp)
    if len(segs) < 2:
        return {'ok': False, 'err': 'seg fail'}
    joined = os.path.join(tdir, 'joined.mp4')
    if not _xfade_join(segs, joined):
        return {'ok': False, 'err': 'join fail'}
    shutil.copy(joined, out)
    if voice_text:
        vp.add_voice(out, voice_text)
    add_music(out, music)
    if caps or hook:
        dur = _dur(out)
        s2 = []
        if hook:
            s2.append((0.0, 2.5, hook))
        if caps:
            st = 2.5 if hook else 0.0
            n2 = len(caps)
            step = (dur - st) / n2 if n2 else dur
            for k, c in enumerate(caps):
                s2.append((st + k * step, st + (k + 1) * step, c))
        vp.add_captions(out, s2, theme or 'default')
    return {'ok': True, 'path': out, 'dur': _dur(out)}