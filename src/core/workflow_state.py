"""Workflow State Management for TNT Media Orchestrator"""
from enum import Enum
from typing import Dict, List, Optional, Any
from datetime import datetime


class WorkflowState(Enum):
    IDLE = "idle"
    PLANNING = "planning"
    GENERATING = "generating"
    REVIEWING = "reviewing"
    APPROVING = "approving"
    PUBLISHING = "publishing"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


class ContentType(Enum):
    MUSIC = "music"
    VIDEO = "video"
    SHORT_FILM = "short_film"
    SERIES = "series"
    SHORTS = "shorts"


class Workflow:
    """Represents a single workflow execution"""
    
    def __init__(self, workflow_id: str, workflow_type: str, params: Dict[str, Any]):
        self.id = workflow_id
        self.type = workflow_type
        self.params = params
        self.state = WorkflowState.PLANNING
        self.created_at = datetime.now()
        self.updated_at = datetime.now()
        self.steps: List[Dict[str, Any]] = []
        self.result: Optional[Any] = None
        self.error: Optional[str] = None
    
    def add_step(self, state: WorkflowState, info: str):
        self.steps.append({
            "state": state.value,
            "info": info,
            "timestamp": datetime.now().isoformat()
        })
        self.updated_at = datetime.now()
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "type": self.type,
            "params": self.params,
            "state": self.state.value,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
            "steps": self.steps,
            "result": self.result,
            "error": self.error
        }
