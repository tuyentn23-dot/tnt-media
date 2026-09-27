# -- coding: utf-8 --
"""Generate read-only follow-up concepts from a winning Shorts pattern."""

MODULE = {
 'name': 'content.viral_followup',
 'version': '1.0.0',
 'interface': 'build(source_metrics: dict) -> dict',
 'config_schema': {'source_metrics': 'dict'},
 'deps': [],
 'health': 'True'
}


def build(source_metrics):
 views = source_metrics.get('views') if isinstance(source_metrics.get('views'), int) else 'unknown'
 duration = source_metrics.get('duration_seconds') if isinstance(source_metrics.get('duration_seconds'), int) else 'unknown'
 return {
 'source_signal': {
 'views': views,
 'duration_seconds': duration,
 'format': 'cute_animal_first_time_reaction',
 'status': 'replicate_structure_not_original'
 },
 'next_clip': {
 'target_duration_seconds': 15,
 'concept': 'Mèo con lần đầu chạm viên đá lạnh và phản ứng bất ngờ',
 'hook_0_1s': 'Cận mặt mèo giật mình ngay frame đầu',
 'beat_1_4s': 'Đưa vật lạ vào khung hình, không giải thích dài',
 'beat_4_10s': '2-3 phản ứng nhanh: ngửi, chạm chân, rụt lại',
 'beat_10_14s': 'Khoảnh khắc đáng yêu hoặc bất ngờ mạnh nhất',
 'beat_14_15s': 'Nối chuyển động cuối về tư thế đầu để tạo loop',
 'caption_options': [
 'Lần đầu bé mèo chạm thứ lạnh thế này 😹',
 'Nó không hiểu chuyện gì vừa xảy ra 🥹',
 'Phản ứng này đúng là không đỡ nổi 😹'
 ]
 },
 'publish_rules': {
 'keep_original_live': True,
 'delete_or_reupload_original': False,
 'buy_fake_engagement': False,
 'reuse_exact_media': False,
 'replicate_story_structure': True
 },
 'measurement': {
 'status': 'no_model_no_forecast',
 'reason': 'no trained model; no view numbers fabricated',
 }
 }


def health():
 return True
