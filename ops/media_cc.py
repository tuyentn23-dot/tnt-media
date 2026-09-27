import os, json, random, urllib.parse
from groq import Groq

_client = None


def _client_get():
 global _client
 if _client is None:
 _client = Groq(api_key=os.environ.get('GROQ_API_KEY'))
 return _client


VISUAL_PROMPT = '''Ban la director hinh anh cho YouTube Shorts.
Chu de video: {topic}
Niche: {niche}
Script:
{script}

Hay de xuat {n} KEYWORD TIM KIEM HINH ANH (tieng Anh, cu the, mo ta dung noi dung dang noi) de lay clip/anh minh hoa CHINH XAC cho tung phan cua video.
Moi keyword phai lien quan TRUC TIEP den noi dung dang noi, KHONG duoc chung chung nhu "life