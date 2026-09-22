# voice_master.py - audio duration + loudness/ducking master (flat)
import os, re, subprocess
from ops import voice_engine as VE
FFMPEG = VE.FFMPEG
DUR_RE = re.compile('Duration: ([0-9]+):([0-9]+):([0-9.]+)')

def duration(path):
 r = subprocess.run([FFMPEG, '-i', path], capture_output=True, text=True)
 m = DUR_RE.search(r.stderr)
 g = m.groups() if m else ('0', '0', '0')
 hh = int(g[0])
 mm = int(g[1])
 ss = float(g[2])
 return hh * 3600 + mm * 60 + ss

def master(vo, out, music=None, music_db=-20):
 has_music = bool(music) and os.path.exists(music)
 fc = '[0:a]loudnorm=I=-14:TP=-1.5:LRA=11[vo];[1:a]volume=' + str(music_db) + 'dB[bg];'
 fc += '[bg][vo]sidechaincompress=threshold=0.03:ratio=8:attack=5:release=300[duck];'
 fc += '[vo][duck]amix=inputs=2:duration=first:weights=1 0.5[out]'
 cmd_m = [FFMPEG, '-y', '-i', vo, '-stream_loop', '-1', '-i', music, '-filter_complex', fc, '-map', '[out]', '-c:a', 'libmp3lame', '-b:a', '192k', out]
 cmd_s = [FFMPEG, '-y', '-i', vo, '-af', 'loudnorm=I=-14:TP=-1.5:LRA=11', '-c:a', 'libmp3lame', '-b:a', '192k', out]
 r = subprocess.run(cmd_m if has_music else cmd_s, capture_output=True, text=True)
 return out if r.returncode == 0 else vo
