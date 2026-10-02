# -- coding: utf-8 --
# app/_routes_prompts.py - Agent mode prompts API
# Tach rieng de giam rui ro sua server.py chinh.
import os, sys
from fastapi import APIRouter
from fastapi.responses import JSONResponse

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)

router = APIRouter()

PROMPTS_DIR = os.path.join(ROOT, 'PLAN', 'prompts')
MODES = ['plan', 'dev', 'run']

MODE_META = {
	'plan': {'name': 'PLAN', 'role': 'Lap ke hoach', 'may': ['Ghi PLAN/', 'Phan tich', 'Ra task'], 'may_not': ['Chay code', 'Sua source', 'Publish']},
	'dev': {'name': 'DEV', 'role': 'Phat trien', 'may': ['Sua source', 'Test co lap', 'Commit'], 'may_not': ['Cham runtime data', 'Publish', 'Sua DB prod']},
	'run': {'name': 'RUN', 'role': 'Van hanh', 'may': ['Chay app', 'Backup', 'Xu ly su co'], 'may_not': ['Sua source']},
}


def _read_prompt(mode):
	path = os.path.join(PROMPTS_DIR, mode.upper() + '_prompt.txt')
	try:
		with open(path, encoding='utf-8') as fh:
			return fh.read()
	except Exception:
		return None


@router.get('/api/agent-prompts')
def agent_prompts():
	out = {}
	for m in MODES:
		p = _read_prompt(m)
		out[m] = {'ok': p is not None, 'prompt': p or ''}
	return JSONResponse({'ok': all(v['ok'] for v in out.values()), 'prompts': out})


@router.get('/api/agent-modes')
def agent_modes():
	return JSONResponse({'ok': True, 'modes': MODE_META, 'invariant': 'source != data != release'})
