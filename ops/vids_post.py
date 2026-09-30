# -- coding: utf-8 --
# Hau ky video: caption thap + voice + nen mau theo chu de.
import os, subprocess, shutil

THEMES = {
    'default': {'back': '&H80000000', 'primary': '&H00FFFFFF'},
    'pink': {'back': '&H60C3C0FF', 'primary': '&H00FFFFFF'},
    'purple': {'back': '&H60FF80C0', 'primary': '&H00FFFFFF'},
    'gold': {'back': '&H6000D7FF', 'primary': '&H00000000'},
    'blue': {'back': '&H60FF8040', 'primary': '&H00FFFFFF'},
    'orange': {'back': '&H6000A5FF', 'primary': '&H00FFFFFF'},
    'brown': {'back': '&H60204060', 'primary': '&H00FFFFFF'},
    'green': {'back': '&H6000A000', 'primary': '&H00FFFFFF'},
    'sunset': {'back': '&H600080FF', 'primary': '&H00FFFFFF'},
}

def _ff():
    root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    ff = os.path.join(root, 'tools', 'ffmpeg.exe')
    return ff if os.path.exists(ff) else 'ffmpeg'

def _ts(t):
    h = int(t // 3600)
    m = int((t % 3600) // 60)
    sec = t % 60
    return str(h).zfill(2) + ':' + str(m).zfill(2) + ':' + ('%06.3f' % sec).replace('.', ',')

def build_srt(segs, out):
    lines = []
    for i, (a, b, tx) in enumerate(segs, 1):
        lines.append(str(i))
        lines.append(_ts(a) + ' --> ' + _ts(b))
        lines.append(tx)
        lines.append('')
    open(out, 'w', encoding='utf-8').write(chr(10).join(lines))
    return out

def add_voice(path, text, voice=None):
    from ops import voice as _v
    vp, _ = _v.synth(text, out_path=os.path.join((os.path.dirname(path) or '.'), '_vo.mp3'), voice=voice)
    if not vp or not os.path.exists(vp):
        return False
    tmp = path + '.vo.mp4'
    fc = '[0:a]volume=0.20[bg];[1:a]volume=1.9[vo];[bg][vo]amix=inputs=2:duration=first:dropout_transition=0'
    cmd = [_ff(), '-y', '-i', path, '-i', vp, '-filter_complex', fc, '-c:v', 'copy', '-c:a', 'aac', '-shortest', tmp]
    r = subprocess.run(cmd, capture_output=True)
    if r.returncode == 0 and os.path.exists(tmp):
        shutil.move(tmp, path)
        return True
    return False

def add_captions(path, segs, theme='default'):
    th = THEMES.get(theme, THEMES['default'])
    srt = os.path.join(os.path.dirname(path), '_cap.srt')
    build_srt(segs, srt)
    tmp = path + '.cap.mp4'
    srt_esc = srt.replace(chr(92), '/').replace(':', chr(92) + ':')
    style = ('FontName=Arial,FontSize=16,Bold=1,PrimaryColour=' + th['primary'] + ',OutlineColour=&H00000000,BackColour=' + th['back'] + ',BorderStyle=4,Outline=2,Shadow=0,MarginV=340,Alignment=2')
    vf = 'subtitles=' + srt_esc + ':force_style=' + chr(39) + style + chr(39)
    cmd = [_ff(), '-y', '-i', path, '-vf', vf, '-c:a', 'copy', tmp]
    r = subprocess.run(cmd, capture_output=True)
    if r.returncode == 0 and os.path.exists(tmp):
        shutil.move(tmp, path)
        return True
    return False
