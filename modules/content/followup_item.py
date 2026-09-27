# -- coding: utf-8 --
"""Validated follow-up content item for Mia Linh Cute; does not publish."""

MODULE={'name':'content.followup_item','version':'1.0.0','interface':'build() -> dict','config_schema':{},'deps':['content.topic_guard'],'health':'True'}


def build():
 return {
 'id':'viral_followup_cat_ice_15s',
 'topic':'cute_animals',
 'hook':'Mèo con lần đầu chạm đá lạnh 😹',
 'body':'Bé mèo tò mò đưa chân chạm viên đá lạnh, giật mình rụt lại rồi vẫn quay lại thử thêm lần nữa.',
 'payoff':'Phản ứng đáng yêu nhất xuất hiện ở cuối và nối về biểu cảm đầu để tạo loop.',
 'duration_seconds':15,
 'format':'9:16',
 'source_strategy':'new_followup_not_reupload',
 'status':'draft'
 }


def validate():
 from modules.content.topic_guard import check
 item=build()
 result=check('cute_animals',item)
 return {'ok':bool(result.get('allowed')),'guard':result,'item':item}


def health():
 return validate()['ok']
