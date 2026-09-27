# -- coding: utf-8 --
"""Production-ready 15-second Shorts script generator for winning cute-animal format."""

MODULE = {
 'name': 'content.viral_script',
 'version': '1.1.0',
 'interface': 'build() -> dict',
 'config_schema': {},
 'deps': [],
 'health': 'True'
}


def build():
 return {
 'duration_seconds': 15,
 'format': '9:16',
 'resolution': '1080x1920',
 'title': 'Mèo con lần đầu chạm đá lạnh 😹',
 'voiceover': [
 {'start': 0.0, 'end': 1.0, 'text': 'Ủa... lạnh gì vậy?'},
 {'start': 1.0, 'end': 3.2, 'text': 'Bé thử chạm một cái...'},
 {'start': 3.2, 'end': 6.2, 'text': 'Ơ! Sao lạnh dữ vậy trời?'},
 {'start': 6.2, 'end': 10.0, 'text': 'Tò mò quá... vẫn phải thử lần nữa!'},
 {'start': 10.0, 'end': 13.5, 'text': 'Nhìn cái mặt kìa 😹'},
 {'start': 13.5, 'end': 15.0, 'text': ''}
 ],
 'shots': [
 {'start': 0.0, 'end': 0.7, 'shot': 'Cận cực gần biểu cảm giật mình mạnh nhất; không fade, không intro', 'text': 'LẠNH GÌ VẬY?!', 'crop': 'face_center'},
 {'start': 0.7, 'end': 2.8, 'shot': 'Mèo nhìn viên đá rồi đưa chân lại gần; zoom nhẹ 105-110%', 'text': 'lần đầu chạm đá lạnh', 'crop': 'face_and_paw'},
 {'start': 2.8, 'end': 5.2, 'shot': 'Chân vừa chạm thì rụt lại; hard cut đúng phản xạ', 'text': 'Ơ KÌA 😹', 'crop': 'paw_closeup'},
 {'start': 5.2, 'end': 8.0, 'shot': 'Cận mặt phản ứng, giữ mắt ở vùng 35-45% chiều cao khung', 'text': 'vẫn tò mò...', 'crop': 'face_center'},
 {'start': 8.0, 'end': 11.5, 'shot': 'Lần chạm thứ hai; 2 cut nhanh giữa chân và mặt', 'text': 'thử thêm lần nữa 😂', 'crop': 'face_and_paw'},
 {'start': 11.5, 'end': 14.2, 'shot': 'Payoff đáng yêu nhất; giữ shot đủ lâu để người xem cảm nhận', 'text': 'cái mặt này 😹', 'crop': 'face_center'},
 {'start': 14.2, 'end': 15.0, 'shot': 'Match pose hoặc hướng nhìn với frame đầu để loop gần như vô hình', 'text': '', 'crop': 'face_center'}
 ],
 'edit_rules': {
 'intro_logo': False,
 'first_reaction_within_seconds': 0.5,
 'max_static_shot_seconds': 2.8,
 'captions_words_per_screen_max': 5,
 'caption_safe_zone_top_pct': 18,
 'caption_safe_zone_bottom_pct': 22,
 'subject_safe_width_pct': 78,
 'music': 'nhịp vui nhẹ, giảm âm khi có phản ứng hoặc voiceover',
 'sfx': '1 hiệu ứng pop nhẹ ở lần rụt chân đầu tiên, không lạm dụng',
 'loop_required': True,
 'reuse_original_media': False,
 'no_fake_engagement': True
 },
 'caption': 'Lần đầu bé mèo chạm đá lạnh và cái kết 😹❄️ #meocon #cutecat #shorts',
 'pinned_comment': 'Mèo nhà bạn gặp cái lạnh lần đầu sẽ phản ứng sao? 😹',
 'success_checks': {
 'hook': 'Phản ứng mạnh xuất hiện trong 0.5 giây đầu',
 'clarity': 'Người xem hiểu tình huống trước giây 2',
 'payoff': 'Khoảnh khắc mạnh nhất nằm khoảng giây 11.5-14.2',
 'loop': 'Frame cuối nối tự nhiên về frame đầu'
 }
 }


def health():
 return True
