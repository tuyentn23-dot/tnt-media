"""YouTube publisher."""

from __future__ import annotations

from .base import BasePublisher, PublishResult

MODULE = {
	'tool': 'youtube-publish',
	'name': 'publish.youtube',
	'version': '1.0.0',
	'interface': 'YouTubePublisher(access_token).publish(content) -> PublishResult',
	'deps': ['ops.os_publish']
}


class YouTubePublisher(BasePublisher):
	def __init__(self, access_token=None) -> None:
		self.access_token = access_token

	def publish(self, content: dict) -> PublishResult:
		if not self.validate(content):
			return PublishResult(False, 'youtube', error='invalid content')
		if not self.access_token:
			return PublishResult(False, 'youtube', error='missing credentials')
		return PublishResult(True, 'youtube', post_id='stub-yt-1')
