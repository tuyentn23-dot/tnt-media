# -- coding: utf-8 --
# app/_test_api.py - Test API bang TestClient
import os, sys, json
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)
from fastapi.testclient import TestClient
from app.server import app

c = TestClient(app)
for path in ['/api/health', '/api/channels', '/api/publications?limit=2', '/api/jobs?limit=2', '/api/quota', '/api/modules']:
	r = c.get(path)
	print(path, '->', r.status_code, json.dumps(r.json(), ensure_ascii=False)[:200])
