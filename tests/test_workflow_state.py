"""Tests for Workflow State Management"""
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

import pytest
from src.core.workflow_state import WorkflowState, Workflow, ContentType


class TestWorkflowState:
    """Test WorkflowState enum"""
    
    def test_valid_states(self):
        assert WorkflowState.IDLE.value == "idle"
        assert WorkflowState.PLANNING.value == "planning"
        assert WorkflowState.GENERATING.value == "generating"
        assert WorkflowState.REVIEWING.value == "reviewing"
        assert WorkflowState.APPROVING.value == "approving"
        assert WorkflowState.PUBLISHING.value == "publishing"
        assert WorkflowState.COMPLETED.value == "completed"
        assert WorkflowState.FAILED.value == "failed"
        assert WorkflowState.CANCELLED.value == "cancelled"
    
    def test_content_types(self):
        assert ContentType.MUSIC.value == "music"
        assert ContentType.VIDEO.value == "video"
        assert ContentType.SHORT_FILM.value == "short_film"
        assert ContentType.SERIES.value == "series"
        assert ContentType.SHORTS.value == "shorts"


class TestWorkflow:
    """Test Workflow class"""
    
    def test_workflow_creation(self):
        wf = Workflow("test_1", "music_generation", {"bpm": 120})
        assert wf.id == "test_1"
        assert wf.type == "music_generation"
        assert wf.params == {"bpm": 120}
        assert wf.state == WorkflowState.PLANNING
    
    def test_add_step(self):
        wf = Workflow("test_2", "video", {})
        wf.add_step(WorkflowState.GENERATING, "Generating video...")
        assert len(wf.steps) == 1
        assert wf.steps[0]["state"] == "generating"
        assert wf.steps[0]["info"] == "Generating video..."
    
    def test_to_dict(self):
        wf = Workflow("test_3", "music", {})
        d = wf.to_dict()
        assert d["id"] == "test_3"
        assert d["type"] == "music"
        assert "created_at" in d
        assert "updated_at" in d


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
