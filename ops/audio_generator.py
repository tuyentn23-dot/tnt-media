import os
import requests
import json

def generate_voiceover(text: str, filename="assets/voiceover.mp3"):
    print('[INFO] Bat dau tao voiceover voi ElevenLabs...')
    api_key = os.getenv("ELEVENLABS_API_KEY")
    voice_id = os.getenv("ELEVENLABS_VOICE_ID", "21m00Tcm4TlvDq8ikWAM") # Rachel voice default
    
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    
    if not api_key:
        print('[WARNING] Thieu ELEVENLABS_API_KEY. Tao file mp3 gia lap de test logic.')
        with open(filename, 'wb') as f: f.write(b"dummy audio")
        return filename
        
    url = f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}"
    headers = {
        "Accept": "audio/mpeg",
        "Content-Type": "application/json",
        "xi-api-key": api_key
    }
    data = {
        "text": text,
        "model_id": "eleven_multilingual_v2",
        "voice_settings": {"stability": 0.5, "similarity_boost": 0.5}
    }
    
    try:
        response = requests.post(url, json=data, headers=headers)
        if response.status_code == 200:
            with open(filename, 'wb') as f:
                f.write(response.content)
            print(f'[SUCCESS] Da luu voiceover tai {filename}')
            return filename
        else:
            print(f'[ERROR] ElevenLabs error: {response.text}')
    except Exception as e:
        print(f'[ERROR] Loi goi ElevenLabs API: {e}')
    return None

def generate_bgm(prompt="instrumental, cinematic, lo-fi, slow tempo, no vocals", filename="assets/bgm.mp3"):
    print(f'[INFO] Bat dau tao BGM voi Suno API (Prompt: {prompt})...')
    api_key = os.getenv("SUNO_API_KEY")
    api_url = os.getenv("SUNO_API_URL", "http://localhost:3000/api/generate") # Dung cho unofficial API wrapper
    
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    
    if not api_key and "localhost" not in api_url:
        print('[WARNING] Thieu config Suno API. Tao file mp3 gia lap de test logic.')
        with open(filename, 'wb') as f: f.write(b"dummy bgm")
        return filename
        
    payload = {
        "prompt": prompt,
        "make_instrumental": True,
        "wait_audio": True
    }
    headers = {"Authorization": f"Bearer {api_key}"} if api_key else {}
    
    try:
        print('[INFO] Dang gui request tao nhac Suno (co the mat 1-2 phut)...')
        response = requests.post(api_url, json=payload, headers=headers)
        if response.status_code == 200:
            # Gia dinh cau truc tra ve co chua audio_url
            audio_url = response.json()[0].get("audio_url")
            if audio_url:
                audio_data = requests.get(audio_url).content
                with open(filename, 'wb') as f:
                    f.write(audio_data)
                print(f'[SUCCESS] Da luu BGM tai {filename}')
                return filename
        print('[WARNING] Khong the lay duoc nhac, tao file dummy.')
        with open(filename, 'wb') as f: f.write(b"dummy bgm")
    except Exception as e:
        print(f'[ERROR] Loi goi Suno API: {e}')
        with open(filename, 'wb') as f: f.write(b"dummy bgm")
    return filename

if __name__ == "__main__":
    print("=== TEST AUDIO GENERATOR ===")
    generate_voiceover("Xin chao, day la he thong tu dong hoa YouTube cua toi.", "assets/test_voice.mp3")
    generate_bgm(filename="assets/test_bgm.mp3")
