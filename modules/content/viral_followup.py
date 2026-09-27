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
 views = int(source_metrics.get('views') or 0)
 duration = int(source_metrics.get('duration_seconds') or 15)
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
 '24h_conservative_views': 18486,
 '24h_working_views': 20742,
 '24h_momentum_views': 22998,
 'interpretation': {
 'below_conservative': 'distribution_slowing',
 'between_conservative_and_momentum': 'healthy',
 'above_momentum': 'strong_acceleration'
 }
 }
 }


def health():
 return True
