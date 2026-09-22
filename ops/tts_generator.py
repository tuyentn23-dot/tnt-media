import os
try:
    from gTTS import gTTS
    HAS_GTTS = True
except ImportError:
    HAS_GTTS = False

def generate_voiceover(script_text: str, output_path: str = "assets/voiceover.mp3") -> str:
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    print(f"[INFO] Dang tao giong doc (TTS) tu kich ban...")
    
    if HAS_GTTS:
        try:
            tts = gTTS(text=script_text, lang='vi', slow=False)
            tts.save(output_path)
            print(f"[SUCCESS] Da luu file giong doc tai: {output_path}")
            return output_path
        except Exception as e:
            print(f"[WARNING] Khong ket noi duoc dich vu TTS online ({e}), chuyen sang tao audio du phong...")
            
    # Fallback offline bang cach tao file wav co ban
    fallback_path = output_path.replace('.mp3', '.wav')
    import wave
    with wave.open(fallback_path, 'w') as wav_file:
        wav_file.setparams((1, 2, 16000, 0, 'NONE', 'not compressed'))
        wav_file.writeframes(b'\x00' * 16000 * 3) # 3 giay audio
    print(f"[INFO] Da tao file audio fallback tai: {fallback_path}")
    return fallback_path
