"""Intellectual Property Model - Original IP management"""
from dataclasses import dataclass, field, asdict
from typing import Dict, List, Optional, Any
from datetime import datetime
import json


@dataclass
class IP:
    """Represents an original intellectual property (series, character, etc.)"""
    ip_id: str
    name: str
    ip_type: str  # series, character, music_group, film, etc.
    description: str = ""
    genre: str = ""
    target_audience: str = ""
    characters: List[Dict[str, Any]] = field(default_factory=list)
    episodes: List[Dict[str, Any]] = field(default_factory=list)
    related_content: List[str] = field(default_factory=list)
    brand_guidelines: Dict[str, Any] = field(default_factory=dict)
    revenue: Dict[str, Any] = field(default_factory=dict)
    created_at: str = field(default_factory=lambda: datetime.now().isoformat())
    updated_at: str = field(default_factory=lambda: datetime.now().isoformat())
    status: str = "active"
    
    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)
    
    def to_json(self) -> str:
        return json.dumps(self.to_dict(), ensure_ascii=False, indent=2)
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'IP':
        return cls(**{k: v for k, v in data.items() if k in cls.__dataclass_fields__})
    
    @classmethod
    def from_json(cls, json_str: str) -> 'IP':
        return cls.from_dict(json.loads(json_str))
    
    def add_character(self, character: Dict[str, Any]):
        """Add character to IP"""
        self.characters.append(character)
        self.updated_at = datetime.now().isoformat()
    
    def add_episode(self, episode: Dict[str, Any]):
        """Add episode to IP"""
        self.episodes.append(episode)
        self.updated_at = datetime.now().isoformat()
    
    def add_related_content(self, content_id: str):
        """Link related content to IP"""
        if content_id not in self.related_content:
            self.related_content.append(content_id)
            self.updated_at = datetime.now().isoformat()
    
    def update_revenue(self, revenue_data: Dict[str, Any]):
        """Update revenue information"""
        self.revenue.update(revenue_data)
        self.updated_at = datetime.now().isoformat()
