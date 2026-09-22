
"""
TNT Media v3 - Gemini Client
Tich hop Gemini 2.5 Flash cho AI content
"""

import json
import requests
from pathlib import Path

class GeminiClient:
    def __init__(self, config_path='tnt_media_v2/config/gemini_config.json'):
        self.config = self._load_config(config_path)
        self.api_keys = self.config.get('api_keys', [])
        self.current_key_idx = 0
        self.model = 'gemini-flash-latest'
        self.base_url = 'https://generativelanguage.googleapis.com/v1beta/models'
    
    def _load_config(self, path):
        p = Path(path)
        if p.exists():
            with open(p, 'r', encoding='utf-8') as f:
                return json.load(f)
        # Thu tim config o vi tri khac
        for alt in ['tnt_media_v3/config/gemini_config.json', 'config/gemini_config.json']:
            alt_p = Path(alt)
            if alt_p.exists():
                with open(alt_p, 'r', encoding='utf-8') as f:
                    return json.load(f)
        return {}
    
    def generate(self, prompt, temperature=0.7, max_tokens=2048):
        for _ in range(len(self.api_keys)):
            key = self.api_keys[self.current_key_idx % len(self.api_keys)]['key']
            self.current_key_idx += 1
            
            url = self.base_url + '/' + self.model + ':generateContent'
            headers = {'Content-Type': 'application/json', 'x-goog-api-key': key}
            data = {
                'contents': [{'parts': [{'text': prompt}]}],
                'generationConfig': {'temperature': temperature, 'maxOutputTokens': max_tokens}
            }
            
            try:
                r = requests.post(url, headers=headers, json=data, timeout=20)
                if r.status_code == 200:
                    result = r.json()
                    if 'candidates' in result and result['candidates']:
                        return result['candidates'][0]['content']['parts'][0]['text']
            except:
                pass
        return ''
    
    def generate_lyrics(self, theme='tinh yeu', style='tru tinh'):
        prompt = 'Hay sang tac loi bai hat tieng Viet chu de ' + theme + ' phong cach ' + style + '. Co diep khuc, gieo van tu nhien.'
        return self.generate(prompt, temperature=0.9, max_tokens=2048)
    
    def generate_script(self, topic, duration=30):
        prompt = 'Hay tao kich ban video YouTube Shorts ' + str(duration) + ' giay cho chu de: ' + topic + '. Co hook manh, cau truc ro rang, CTA cuoi.'
        return self.generate(prompt, temperature=0.7, max_tokens=2048)
    
    def optimize_seo(self, title):
        prompt = 'Hay toi uu SEO cho video: ' + title + '. Tao 3 tieu de thay the, 10 tags, description.'
        return self.generate(prompt, temperature=0.5, max_tokens=1024)
