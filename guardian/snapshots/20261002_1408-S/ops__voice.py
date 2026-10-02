# -- coding: utf-8 --
import os
import sys
import asyncio
import time
F = '__file__'
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(globals()[F])))
sys.path.insert(0, ROOT)
DEFAULT_VOICE = 'vi-VN-HoaiMyNeural'
VOICE_BY_LANG = dict([('vi', 'vi-VN-HoaiMyNeural'), ('en', 'en-US-AriaNeural')])

def pick_voice(lang=None):
    if not lang:
        return DEFAULT_VOICE
    return VOICE_BY_LANG.get(lang, DEFAULT_VOICE)

def synth(text, out_path=None, voice=None, retries=3):
    import edge_tts
    text = (text or '').strip()
    if not text:
        return None, []
    if out_path is None:
        out_path = os.path.join(ROOT, 'assets', 'voice.mp3')
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    voice = voice or DEFAULT_VOICE
    last = None
    for attempt in range(retries):
        try:
            c = edge_tts.Communicate(text, voice)
            async def go():
                return [ch async for ch in c.stream()]
            chunks = asyncio.run(go())
            audio = b''.join(ch['data'] for ch in chunks if ch.get('type') == 'audio')
            if len(audio) < 2000:
                raise RuntimeError('voice too small')
            f = open(out_path, 'wb')
            f.write(audio)
            f.close()
            sentences = []
            for ch in chunks:
                if ch.get('type') == 'SentenceBoundary':
                    st = ch['offset'] / 1e7
                    du = ch['duration'] / 1e7
                    sentences.append(dict(text=ch['text'], start=st, end=st + du))
            return out_path, sentences
        except Exception as e:
            last = e
            time.sleep(2)
    raise RuntimeError('voice synth failed: ' + str(last))

def sentence_lines(sentences):
    out = []
    for s in sentences or []:
        t = (s.get('text') or '').strip()
        if t:
            out.append((t, float(s.get('start', 0.0)), float(s.get('end', 0.0))))
    return out