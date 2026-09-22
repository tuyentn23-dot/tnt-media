"""Campaign Model - Marketing & promotion campaigns"""
from dataclasses import dataclass, field, asdict
from typing import Dict, List, Optional, Any
from datetime import datetime
import json


@dataclass
class Campaign:
    """Represents a marketing/promotion campaign"""
    campaign_id: str
    name: str
    objective: str  # awareness, engagement, conversion, etc.
    platform: str = "youtube"
    budget: float = 0.0
    start_date: Optional[str] = None
    end_date: Optional[str] = None
    target_metrics: Dict[str, Any] = field(default_factory=dict)
    actual_metrics: Dict[str, Any] = field(default_factory=dict)
    content_ids: List[str] = field(default_factory=list)
    status: str = "planned"  # planned, active, completed, paused, cancelled
    notes: str = ""
    created_at: str = field(default_factory=lambda: datetime.now().isoformat())
    updated_at: str = field(default_factory=lambda: datetime.now().isoformat())
    
    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)
    
    def to_json(self) -> str:
        return json.dumps(self.to_dict(), ensure_ascii=False, indent=2)
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Campaign':
        return cls(**{k: v for k, v in data.items() if k in cls.__dataclass_fields__})
    
    @classmethod
    def from_json(cls, json_str: str) -> 'Campaign':
        return cls.from_dict(json.loads(json_str))
    
    def add_content(self, content_id: str):
        """Add content to campaign"""
        if content_id not in self.content_ids:
            self.content_ids.append(content_id)
            self.updated_at = datetime.now().isoformat()
    
    def update_metrics(self, metrics: Dict[str, Any]):
        """Update actual metrics"""
        self.actual_metrics.update(metrics)
        self.updated_at = datetime.now().isoformat()
    
    def start(self):
        """Start campaign"""
        self.status = "active"
        self.start_date = datetime.now().isoformat()
        self.updated_at = datetime.now().isoformat()
    
    def complete(self):
        """Complete campaign"""
        self.status = "completed"
        self.end_date = datetime.now().isoformat()
        self.updated_at = datetime.now().isoformat()
    
    def pause(self):
        """Pause campaign"""
        self.status = "paused"
        self.updated_at = datetime.now().isoformat()
    
    def cancel(self):
        """Cancel campaign"""
        self.status = "cancelled"
        self.updated_at = datetime.now().isoformat()
