"""Channel Model - YouTube/TikTok channel representation"""
from dataclasses import dataclass, field, asdict
from typing import Dict, List, Optional, Any
from datetime import datetime
import json


@dataclass
class Channel:
    """Represents a social media channel"""
    channel_id: str
    name: str
    platform: str  # youtube, tiktok, facebook, etc.
    description: str = ""
    niche: str = ""
    target_audience: str = ""
    branding: Dict[str, str] = field(default_factory=dict)
    statistics: Dict[str, Any] = field(default_factory=dict)
    tags: List[str] = field(default_factory=list)
    content_calendar: List[Dict[str, Any]] = field(default_factory=list)
    created_at: str = field(default_factory=lambda: datetime.now().isoformat())
    updated_at: str = field(default_factory=lambda: datetime.now().isoformat())
    is_active: bool = True
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for JSON serialization"""
        return asdict(self)
    
    def to_json(self) -> str:
        """Convert to JSON string"""
        return json.dumps(self.to_dict(), ensure_ascii=False, indent=2)
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Channel':
        """Create Channel from dictionary"""
        return cls(**{k: v for k, v in data.items() if k in cls.__dataclass_fields__})
    
    @classmethod
    def from_json(cls, json_str: str) -> 'Channel':
        """Create Channel from JSON string"""
        return cls.from_dict(json.loads(json_str))
    
    def update_statistics(self, stats: Dict[str, Any]):
        """Update channel statistics"""
        self.statistics.update(stats)
        self.updated_at = datetime.now().isoformat()
    
    def add_to_calendar(self, event: Dict[str, Any]):
        """Add content calendar event"""
        self.content_calendar.append(event)
        self.updated_at = datetime.now().isoformat()
    
    def deactivate(self):
        """Deactivate channel"""
        self.is_active = False
        self.updated_at = datetime.now().isoformat()
    
    def activate(self):
        """Activate channel"""
        self.is_active = True
        self.updated_at = datetime.now().isoformat()
