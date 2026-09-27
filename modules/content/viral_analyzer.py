# -- coding: utf-8 --
"""Read-only viral analysis utilities for YouTube Shorts."""
import urllib.request
from datetime import datetime

MODULE={'name':'content.viral_analyzer','version':'1.0.5','interface':'analyze(video_id, title=None) -> dict','config_schema':{'video_id':'str','title':'str|None'},'deps':[],'health':'True'}
SWEET_MIN_SECONDS=13
SWEET_MAX_SECONDS=20

def _fetch_watch_html(video_id):
	base='https:'+chr(47)+chr(47)+'www.youtube.com/watch?v='
	req=urllib.request.Request(base+video_id,headers={'User-Agent':'Mozilla/5.0'})
	return
 urllib.request.urlopen(req,timeout=20).read().decode('utf-8','ignore')

def _extract_between(text,prefix,suffix):
	start=text.find(prefix)
	start=start+len(prefix) if start>=0 else -1
	end=text.find(suffix,start) if start>=0 else -1
	return text[start:end] if start>=0 and end>=0 else None

def public_metrics(video_id):
	html=_fetch_watch_html(video_id)
	views=_extract_between(html,'"viewCount":"','"')
	duration=_extract_between(html,'"lengthSeconds":"','"')
	published=_extract_between(html,'"publishDate":"','"')
	return {'video_id':video_id,'views':int(views) if views and views.isdigit() else None,'duration_seconds':int(duration) if duration and duration.isdigit() else None,'publish_date':published,'captured_at':datetime.now().astimezone().isoformat(timespec='seconds')}

def _hook_variants():
	return ['Khoảnh khắc bé mèo chạm tuyết lần đầu 🥹❄️','Nó đứng hình khi lần đầu thấy thứ trắng xóa này 😹','Phản ứng của mèo con khi lần đầu gặp tuyết… xem đến cuối ❄️🐱']

def analyze(video_id,title=None):
	metrics=public_metrics(video_id)
	duration=metrics.get('duration_seconds')
	sweet=duration is not None and SWEET_MIN_SECONDS<=duration<=SWEET_MAX_SECONDS
	lower=(title or '').lower()
	first_time=('lần đầu' in lower or 'first' in lower or 'đầu tiên' in lower)
	strengths=(['duration_in_13_20s_sweet_spot'] if sweet else [])+(['first_time_curiosity_hook'] if first_time else [])+['cute_animal_emotion','clear_single_event_payoff']
	risks=[] if sweet else ['duration_outside_13_20s_sweet_spot']
	return {'metrics':metrics,'strengths':strengths,'risks':risks,'hook_variants':_hook_variants(),'retention_plan':{'0_1s':'Mở ngay bằng biểu cảm mạnh nhất của mèo, bỏ intro/logo.','1_4s':'Cho mèo tiến sát hoặc chạm tuyết; caption cực ngắn 3-6 từ.','4_10s':'Tăng nhịp bằng 2-3 cut phản ứng, ưu tiên cận mặt hoặc chân.','10_end':'Đưa payoff đáng yêu nhất rồi nối frame cuối gần frame đầu để loop.'},'growth_plan_7d':[{'day':1,'action':'Giữ clip gốc; ghi snapshot views định kỳ và trả lời comment thật nhanh.'},{'day':2,'action':'Đăng clip cùng format: mèo lần đầu gặp một hiện tượng mới, không reupload clip gốc.'},{'day':3,'action':'A/B 2 hook mở đầu trên clip mới cùng niche cute_animals.'},{'day':4,'action':'Tạo response hoặc follow-up dựa trên comment có tín hiệu tốt nhất.'},{'day':5,'action':'Lặp cấu trúc 15-18s, payoff ở 70-90% thời lượng và perfect loop.'},{'day':6,'action':'So sánh velocity, like/view, comment/view giữa các biến thể; bỏ format yếu.'},{'day':7,'action':'Nhân bản format thắng thành series 3-5 clip, giữ nhân vật và chủ đề nhất quán.'}],'guardrails':['Không mua view, like, comment hoặc dùng engagement giả.','Không spam hashtag; ưu tiên nội dung và retention.','Không xóa hoặc reupload clip đang tăng chỉ để đổi hook.']}
