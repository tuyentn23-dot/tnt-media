import os, json, random, time
from groq import Groq

_client = None

def _client_get():
 global _client
 if _client is None:
 _client = Groq(api_key=os.environ.get('GROQ_API_KEY'))
 return _client

# Per-niche seed pools used ONLY as creative direction, not as final topics.
NICHE_SEEDS = {
 'life hacks': ['nha bep', 'don dep', 'tiet kiem dien', 'bao quan thuc pham', 'meo vesinh', 'to chuc nha', 'sua chua nhanh', 'an toan gia dinh'],
 'motivation': ['ky luat ban than', 'vuot kho', 'thoi quen 5h sang', 'tap trung sau', 'tu duy trieu phu', 'chong tri hoan', 'muc tieu 90 ngay', 'confidence'],
 'general': ['kham pha', 'bi quyet', 'su that', 'meo', 'xu huong'],
}

_PROMPT = '''Ban la chuyen gia trend YouTube Shorts thi truong Viet Nam.
Niche: {niche}
Ngon ngu: {lang}

Hay de xuat {n} CHU DE CUC KY CU THE, MOI, CO TINH VIRAL cho Shorts.
YEU CAU:
- Moi chu de phai la 1 cau hanh dong / tinh huong CU THE (vi du: "3 meo bao quan rau muong tuoi 7 ngay khong can tu lanh"), KHONG duoc chung chung kieu "meo hay