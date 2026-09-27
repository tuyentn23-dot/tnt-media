# 3 LOI CRITICAL - DA XAC MINH CODE

## 2.1. [CRITICAL] Publish bo qua quality gate

File: app/_routes_publish.py dong 38
Bang chung da xac minh:

r = os_publish.publish(vp, title, description='', tags=[], privacy=privacy, topic=row['topic'] or '', force=True)


Hau qua:
- Bo qua quality gate chan (score threshold)
- Bo qua kiem tra trung topic
- Tham so force endpoint (dong 25, 27) cho phep bo qua approved
- Neu video_health.check raise exception -> uploader cho di (os_publish.py dong 63-64)

Sua:
python
# _routes_publish.py dong 38 - doi force=True thanh force=force
r = os_publish.publish(vp, title, description='', tags=[], privacy=privacy, topic=row['topic'] or '', force=force)


Trong ops/os_publish.py dong 63-64:
python
# Truoc:
except Exception as _he:
 pass
# Sau:
except Exception as _he:
 return {'ok': False, 'blocked': True, 'reason': 'video-health error: ' + str(_he)[:200]}


## 2.2. [CRITICAL] Route publish trung

Bang chung da xac minh:
- app/_routes_publish.py dong 17: publish_pub(pub_id, privacy, force) (router moi, dang ky TRUOC)
- app/server.py dong 219-220: @app.post('/api/publications/{pub_id}/publish') def publish_pub(pub_id) (ban cu)

Sua: Xoa handler cu trong app/server.py:
- Xoa dong 219-220 va toan bo than ham publish_pub cu
- Kiem tra dong 219-260 de biet het pham vi

## 2.3. [CRITICAL] Chua chong dang trung

File: app/_routes_publish.py dong 24-31
Van de: Doc row['status'] -> kiem tra -> UPDATE status='publishing'. Khong atomic.
Hau qua: 2 request dong thoi cung doc approved -> 2 video tren YouTube.

Sua (thay khoi dong 24-31):
python
res = c.execute("UPDATE publications SET status='publishing' WHERE id=? AND status='approved'", (pub_id,))
if res.rowcount == 0:
 c.commit()
 return JSONResponse({'ok': False, 'error': 'conflict: dang duoc xu ly hoac chua approved'}, status_code=409)
c.commit()


Xu ly them: upload thanh cong nhung mat ket noi truoc khi ghi DB:
- Them cot youtube_id_pending hoac published_at_pending
- Job recovery doi soat YouTube (query theo title+timestamp)
