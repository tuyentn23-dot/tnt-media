"""TNT Media Worker - Background Task Processor"""
import os
import sys
import json
import time
import logging
from datetime import datetime
from typing import Dict, Any, Optional
from pathlib import Path

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.utils.logger import TNTLogger
from src.utils.config import ConfigManager


class MediaWorker:
    """
    Background worker for processing media tasks.
    Handles: music generation, video processing, publishing, etc.
    """
    
    def __init__(self, queue_dir: str = "queue"):
        self.logger = TNTLogger()
        self.config = ConfigManager()
        self.queue_dir = Path(queue_dir)
        self.queue_dir.mkdir(exist_ok=True)
        self.running = True
    
    def process_task(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process a single task.
        This is where the actual work happens.
        """
        task_type = task.get("type")
        task_data = task.get("data", {})
        
        self.logger.log_event(
            "worker",
            f"Processing task: {task_type}",
            task_type=task_type
        )
        
        # TODO: Implement task processing logic
        # This will be connected to the actual media generation modules
        
        result = {
            "success": True,
            "task_type": task_type,
            "processed_at": datetime.now().isoformat()
        }
        
        return result
    
    def run(self):
        """Main worker loop"""
        self.logger.log_event("worker", "Worker started")
        print("TNT Media Worker started. Press Ctrl+C to stop.")
        
        try:
            while self.running:
                # Check for new tasks
                tasks = list(self.queue_dir.glob("*.json"))
                
                if tasks:
                    for task_file in tasks:
                        try:
                            with open(task_file, 'r', encoding='utf-8') as f:
                                task = json.load(f)
                            
                            # Process task
                            result = self.process_task(task)
                            
                            # Save result
                            result_file = task_file.with_suffix('.result.json')
                            with open(result_file, 'w', encoding='utf-8') as f:
                                json.dump(result, f, indent=2, ensure_ascii=False)
                            
                            # Remove task file
                            task_file.unlink()
                            
                            self.logger.log_event(
                                "worker",
                                f"Task completed: {task.get('type')}",
                                result=result
                            )
                        except Exception as e:
                            self.logger.log_error(e, f"Failed to process {task_file}")
                else:
                    # No tasks, wait
                    time.sleep(5)
        except KeyboardInterrupt:
            self.logger.log_event("worker", "Worker stopped by user")
            print("\nWorker stopped.")
        finally:
            self.running = False
    
    def stop(self):
        """Stop the worker"""
        self.running = False
        self.logger.log_event("worker", "Worker stop requested")


if __name__ == '__main__':
    worker = MediaWorker()
    worker.run()
