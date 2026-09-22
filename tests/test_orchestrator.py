"""Tests for TNT Media Orchestrator"""
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

import pytest
from src.core.orchestrator import TNTMediaOrchestrator
from src.core.workflow_state import WorkflowState


class TestOrchestrator:
    """Test TNTMediaOrchestrator"""
    
    @pytest.fixture
    def orchestrator(self, tmp_path):
        """Create a temporary orchestrator"""
        return TNTMediaOrchestrator(workspace_root=str(tmp_path))
    
    def test_start_workflow(self, orchestrator):
        workflow_id = orchestrator.start_workflow(
            "music_generation",
            {"bpm": 120}
        )
        assert workflow_id.startswith("WF_")
        assert orchestrator.current_workflow is not None
        assert orchestrator.current_workflow.type == "music_generation"
    
    def test_update_state(self, orchestrator):
        orchestrator.start_workflow("test", {})
        orchestrator.update_state(WorkflowState.GENERATING, "Generating...")
        assert orchestrator.current_workflow.state == WorkflowState.GENERATING
        assert len(orchestrator.current_workflow.steps) == 2
    
    def test_approve_publish(self, orchestrator):
        orchestrator.start_workflow("test", {})
        # Chưa ở REVIEWING state, không thể approve
        assert orchestrator.approve_publish() == False
        
        # Chuyển sang REVIEWING
        orchestrator.update_state(WorkflowState.REVIEWING)
        assert orchestrator.approve_publish() == True
        assert orchestrator.current_workflow.state == WorkflowState.APPROVING
    
    def test_complete_workflow(self, orchestrator):
        orchestrator.start_workflow("test", {})
        orchestrator.update_state(WorkflowState.REVIEWING)
        orchestrator.approve_publish()
        orchestrator.complete_workflow({"result": "success"})
        assert orchestrator.current_workflow is None
        assert len(orchestrator.workflow_history) == 1
    
    def test_fail_workflow(self, orchestrator):
        orchestrator.start_workflow("test", {})
        orchestrator.fail_workflow("Test error")
        assert orchestrator.current_workflow is None
        assert len(orchestrator.workflow_history) == 1
        assert orchestrator.workflow_history[0].error == "Test error"
    
    def test_save_and_load_state(self, orchestrator):
        orchestrator.start_workflow("test", {})
        orchestrator.save_state()
        assert orchestrator.load_state() == True


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
