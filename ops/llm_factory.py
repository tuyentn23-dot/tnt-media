import requests
import json

class ResultWrapper:
    def __init__(self, c):
        self.content = c

class SimpleOllamaLLM:
    def __init__(self, model="llama3.2:1b", base_url="http://127.0.0.1:11434"):
        self.model = model
        self.base_url = base_url

    def invoke(self, prompt_text):
        url = f"{self.base_url}/api/generate"
        payload = {
            "model": self.model,
            "prompt": prompt_text,
            "stream": False,
            "options": {
                "num_predict": 100,
                "temperature": 0.3
            }
        }
        try:
            response = requests.post(url, json=payload, timeout=90)
            if response.status_code == 200:
                res_json = response.json()
                content = res_json.get("response", "")
                return ResultWrapper(content)
            else:
                return ResultWrapper(f"Xu huong AI va tu dong hoa thong minh 2026")
        except Exception as e:
            return ResultWrapper(f"Xu huong AI va tu dong hoa thong minh 2026")

def get_local_llm():
    return SimpleOllamaLLM()
