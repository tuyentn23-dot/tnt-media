"""Content loader."""

from __future__ import annotations

import json
from pathlib import Path

MODULE = {
	'tool': 'content-loader',
	'name': 'content.loader',
	'version': '1.0.0',
	'interface': 'ContentLoader(data_dir).load_json(name) -> dict',
	'deps': []
}


class ContentLoader:
	def __init__(self, data_dir='data/content') -> None:
		self.data_dir = Path(data_dir)

	def load_json(self, name):
		path = self.data_dir / name
		if not path.exists():
			return None
		with path.open(encoding='utf-8') as fh:
			return json.load(fh)
