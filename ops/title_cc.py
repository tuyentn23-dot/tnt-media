import os, json, random
from groq import Groq

_client = None


def _client_get():
 global _client
 if _client is None:
 _client = Groq(api_key=os.environ.get('GROQ_API_KEY'))
 return _client


PROMPT = '''Ban la chuyen gia viet tieu de viral YouTube Shorts tieng Viet.
Chu de: {topic}
Niche: {niche}
Hook cua script: {hook}

Hay viet {n} TIEU DE hoan toan khac nhau cho video nay.
YEU CAU BAT BUOC:
- Tieng Viet tu nhien, co dau, KHONG duoc tra ve nguyen van chu de.
- Do dai 40-70 ky tu, co so lieu / con so / thoi gian / ket qua cu the neu phu hop.
- Tao to mo / toang / toang: dung cac pattern nhu "Sai lam...