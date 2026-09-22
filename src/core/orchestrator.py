"""TNT Media Orchestrator - Central Controller"""
import json
import logging
import os
from typing import Dict, List, Optional, Any
from .workflow_state import WorkflowState, Workflow

logger = logging.getLogger(__name__)


class TNTMediaOrchestrator:
    """Single final orchestrator for TNT Media"""
    
    def __init__(self, workspace_root: str = "."):
        self.workspace_root = workspace_root
        self.current_workflow: Optional[Workflow] = None
        self.workflow_history: List[Workflow] = []
        
        os.makedirs(os.path.join(workspace_root, "logs"), exist_ok=True)
        os.makedirs(os.path.join(workspace_root, "memory"), exist_ok=True)
        
        logging.basicConfig(
            filename=os.path.join(workspace_root, "logs", "orchestrator.log"),
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s'
        )
        
        logger.info("TNT Media Orchestrator initialized")
    
    def start_workflow(self, workflow_type: str, params: Dict[str, Any]) -> str:
        """Start new workflow"""
        from datetime import datetime
        workflow_id = f"WF_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        self.current_workflow = Workflow(workflow_id, workflow_type, params)
        self.current_workflow.add_step(WorkflowState.PLANNING, "Workflow started")
        
        logger.info(f"Workflow {workflow_id} started: {workflow_type}")
        return workflow_id
    
    def update_state(self, new_state: WorkflowState, info: str = ""):
        if self.current_workflow:
            self.current_workflow.state = new_state
            self.current_workflow.add_step(new_state, info)
            logger.info(f"{self.current_workflow.id} -> {new_state.value}: {info}")
    
    def approve_publish(self) -> bool:
        """Final decision - only orchestrator can approve publish"""
        if not self.current_workflow:
            return False
        if self.current_workflow.state != WorkflowState.REVIEWING:
            logger.warning("Cannot approve - workflow not in REVIEWING state")
            return False
        
        self.update_state(WorkflowState.APPROVING, "Approved by orchestrator")
        return True
    
    def complete_workflow(self, result: Any):
        if self.current_workflow:
            self.current_workflow.result = result
            self.current_workflow.state = WorkflowState.COMPLETED
            self.workflow_history.append(self.current_workflow)
            logger.info(f"Workflow {self.current_workflow.id} completed")
            self.current_workflow = None
    
    def fail_workflow(self, error: str):
        if self.current_workflow:
            self.current_workflow.error = error
            self.current_workflow.state = WorkflowState.FAILED
            self.workflow_history.append(self.current_workflow)
            logger.error(f"Workflow {self.current_workflow.id} failed: {error}")
            self.current_workflow = None
    
    def get_status(self) -> Dict[str, Any]:
        if self.current_workflow:
            return {
                "active": True,
                "workflow": self.current_workflow.to_dict()
            }
        return {
            "active": False,
            "history_count": len(self.workflow_history)
        }
    
    def save_state(self, filename: str = "orchestrator_state.json"):
        """Persist orchestrator state"""
        state = {
            "current_workflow": self.current_workflow.to_dict() if self.current_workflow else None,
            "history": [w.to_dict() for w in self.workflow_history[-100:]],
            "saved_at": str(__import__('datetime').datetime.now())
        }
        filepath = os.path.join(self.workspace_root, "memory", filename)
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(state, f, indent=2, ensure_ascii=False)
        logger.info(f"State saved to {filepath}")
    
    def load_state(self, filename: str = "orchestrator_state.json") -> bool:
        """Restore orchestrator state"""
        filepath = os.path.join(self.workspace_root, "memory", filename)
        if not os.path.exists(filepath):
            logger.warning(f"State file not found: {filepath}")
            return False
        
        with open(filepath, 'r', encoding='utf-8') as f:
            state = json.load(f)
        
        if state.get("current_workflow"):
            wf_data = state["current_workflow"]
            self.current_workflow = Workflow(
                wf_data["id"],
                wf_data["type"],
                wf_data["params"]
            )
            self.current_workflow.state = WorkflowState(wf_data["state"])
            self.current_workflow.result = wf_data.get("result")
            self.current_workflow.error = wf_data.get("error")
        
        logger.info(f"State restored from {filepath}")
        return True
