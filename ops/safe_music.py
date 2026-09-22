# safe_music.py - 100% copyright-free algorithmic music (numpy+wave)
import os, sys, wave
import numpy as np
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SR = 44100

def note(freq, dur, wave_type="sine", amp=0.3):
    t = np.linspace(0, dur, int(SR*dur), False)
    if wave_type == "sine":
        y = np.sin(2*np.pi*freq*t)
    elif wave_type == "tri":
        y = 2*np.abs(2*((t*freq)%1)-1)-1
    else:
        y = np.sign(np.sin(2*np.pi*freq*t))
    env = np.minimum(1, np.minimum(t*20, (dur-t)*20))
    return amp*y*env

def kick(dur=0.15):
    t = np.linspace(0, dur, int(SR*dur), False)
    f = 120*np.exp(-t*30)+40
    y = np.sin(2*np.pi*np.cumsum(f)/SR)
    return 0.6*y*np.exp(-t*12)

def hat(dur=0.05):
    t = np.linspace(0, dur, int(SR*dur), False)
    return 0.15*np.random.randn(len(t))*np.exp(-t*60)

def build_track(scale, bpm=100, bars=8):
    beat = 60.0/bpm
    total = int(SR*beat*4*bars)
    out = np.zeros(total)
    step = beat/2
    seq = [scale[i % len(scale)] for i in range(bars*8)]
    for i, f in enumerate(seq):
        pos = int(i*step*SR)
        if pos >= total: break
        seg = note(f, step*0.9, "tri", 0.22)
        out[pos:pos+len(seg)] += seg[:total-pos]
    for b in range(bars*4):
        pos = int(b*beat*SR)
        k = kick()
        out[pos:pos+len(k)] += k[:total-pos]
    for b in range(bars*8):
        pos = int(b*step*SR)
        h = hat()
        out[pos:pos+len(h)] += h[:total-pos]
    out = np.tanh(out*0.8)
    out = (out*32767).astype(np.int16)
    return out

def write_wav(samples, path):
    st = np.column_stack([samples, samples])
    w = wave.open(path, "wb")
    w.setnchannels(2)
    w.setsampwidth(2)
    w.setframerate(SR)
    w.writeframes(st.tobytes())
    w.close()

SCALES = {"food": [392,440,494,523,587,523,494,440], "cat": [523,587,659,698,659,587,523,494], "dog": [330,392,440,392,330,294,330,392], "magic": [440,523,659,784,659,523,440,392], "satisfying": [349,440,523,440,349,294,349,440]}

def generate(topic, out=None):
    out = out or os.path.join(ROOT, "library", "music_"+topic+".wav")
    freqs = SCALES.get(topic, SCALES["food"])
    samples = build_track(freqs)
    write_wav(samples, out)
    return out

if __name__ == "__main__":
    for t in ["food","cat","dog","magic","satisfying"]:
        print(generate(t))
