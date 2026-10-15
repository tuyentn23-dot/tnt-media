# app/_routes_analyze.py - Router phan tich video (scene + quality)
import os, sys
from fastapi import APIRouter, Query
from fastapi.responses import JSONResponse, FileResponse

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)
router = APIRouter()

OUTPUT_ROOT = os.path.join(ROOT, 'output')
REPORTS_ROOT = os.path.join(ROOT, 'reports')


def _safe_path(name):
	p = os.path.abspath(os.path.join(OUTPUT_ROOT, os.path.basename(name or '')))
	if not p.startswith(os.path.abspath(OUTPUT_ROOT)):
		return None
	return p if os.path.exists(p) else None


@router.get('/api/analyze/quick')
def analyze_quick(name: str = Query(...)):
	fp = _safe_path(name)
	if not fp:
		return JSONResponse({'ok': False, 'error': 'file not found'}, status_code=404)
	try:
		from ops import video_reader as vr
		r = vr.read_video(fp, n_frames=6, use_vision=False)
		return {'ok': r.get('ok'), 'duration': r.get('duration'), 'avg_brightness': r.get('avg_brightness'), 'black_frames': r.get('black_frames'), 'issues': r.get('issues', [])}
	except Exception as e:
		return JSONResponse({'ok': False, 'error': str(e)[:300]}, status_code=500)


@router.get('/api/analyze/video')
def analyze_video_endpoint(name: str = Query(...), vision: int = 0):
	fp = _safe_path(name)
	if not fp:
		return JSONResponse({'ok': False, 'error': 'file not found'}, status_code=404)
	try:
		from ops import video_analyzer as va
		report_dir = os.path.join(REPORTS_ROOT, 'analysis_' + os.path.splitext(os.path.basename(fp))[0])
		r = va.analyze_video(fp, output=report_dir, use_vision=bool(vision))
		return {'ok': True, 'scenes': len(r.get('scenes', [])), 'duration': r.get('duration'), 'vision_completed': r.get('vision_completed', 0), 'report_dir': os.path.relpath(report_dir, ROOT)}
	except Exception as e:
		return JSONResponse({'ok': False, 'error': str(e)[:300]}, status_code=500)


@router.get('/api/analyze/report')
def analyze_report(name: str = Query(...), file: str = Query('index.html')):
	safe_name = os.path.basename(name)
	safe_file = os.path.basename(file)
	rep = os.path.join(REPORTS_ROOT, 'analysis_' + os.path.splitext(safe_name)[0], safe_file)
	if not os.path.exists(rep):
		return JSONResponse({'ok': False, 'error': 'report not found - chay /api/analyze/video truoc'}, status_code=404)
	mime = 'image/jpeg' if safe_file.endswith('.jpg') else 'text/html'
	return FileResponse(rep, media_type=mime)
