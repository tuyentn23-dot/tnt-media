"""Content Model - Media content representation"""
from dataclasses import dataclass, field, asdict
from typing import Dict, List, Optional, Any
from datetime import datetime
import json


@dataclass
class Content:
    """Represents a media content item (video, music, short, etc.)"""
    content_id: str
    title: str
    content_type: str  # music, video, short, series, etc.
    platform: str = "youtube"
    status: str = "draft"  # draft, generated, reviewing, approved, published
    description: str = ""
    tags: List[str] = field(default_factory=list)
    file_path: Optional[str] = None
    thumbnail_path: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)
    performance: Dict[str, Any] = field(default_factory=dict)
    ip_reference: Optional[str] = None  # Reference to IP model
    campaign_id: Optional[str] = None
    created_at: str = field(default_factory=lambda: datetime.now().isoformat())
    updated_at: str = field(default_factory=lambda: datetime.now().isoformat())
    published_at: Optional[str] = None
    
    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)
    
    def to_json(self) -> str:
        return json.dumps(self.to_dict(), ensure_ascii=False, indent=2)
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Content':
        return cls(**{k: v for k, v in data.items() if k in cls.__dataclass_fields__})
    
    @classmethod
    def from_json(cls, json_str: str) -> 'Content':
        return cls.from_dict(json.loads(json_str))
    
    def publish(self):
        """Mark content as published"""
        self.status = "published"
        self.published_at = datetime.now().isoformat()
        self.updated_at = datetime.now().isoformat()
    
    def update_performance(self, metrics: Dict[str, Any]):
        """Update performance metrics (views, likes, etc.)"""
        self.performance.update(metrics)
        self.updated_at = datetime.now().isoformat()
    
    def add_tag(self, tag: str):
        """Add a tag"""
        if tag not in self.tags:
            self.tags.append(tag)
            self.updated_at = datetime.now().isoformat()
    
    def set_file(self, file_path: str):
        """Set content file path"""
        self.file_path = file_path
        self.updated_at = datetime.now().isoformat()
    
    def set_thumbnail(self, thumbnail_path: str):
        """Set thumbnail path"""
        self.thumbnail_path = thumbnail_path
        self.updated_at = datetime.now().isoformat()
