"""Service Registry for TNT Media Operations"""
import importlib
import sys
import os
from typing import Dict, Any, Optional, List


class ServiceRegistry:
    """Registry for all specialist services"""
    
    def __init__(self, ops_path: str = "ops"):
        self.ops_path = ops_path
        self.services: Dict[str, Dict[str, Any]] = {}
    
    def scan_services(self):
        """Scan all ops modules and register them"""
        if not os.path.exists(self.ops_path):
            return
        
        sys.path.insert(0, os.getcwd())
        
        for filename in os.listdir(self.ops_path):
            if filename.endswith('.py') and not filename.startswith('__'):
                module_name = filename.replace('.py', '')
                try:
                    module = importlib.import_module(f'ops.{module_name}')
                    
                    classes = []
                    for name, obj in module.__dict__.items():
                        if isinstance(obj, type) and obj.__module__ == module.__name__:
                            classes.append(name)
                    
                    self.services[module_name] = {
                        'module': module,
                        'classes': classes,
                        'loaded': True,
                        'error': None
                    }
                except Exception as e:
                    self.services[module_name] = {
                        'module': None,
                        'classes': [],
                        'loaded': False,
                        'error': str(e)
                    }
    
    def get_service(self, name: str):
        """Get a service by name"""
        return self.services.get(name)
    
    def list_services(self) -> List[Dict[str, Any]]:
        """List all registered services"""
        return [
            {
                'name': name,
                'loaded': info['loaded'],
                'classes': info['classes'],
                'error': info.get('error')
            }
            for name, info in self.services.items()
        ]
    
    def get_loaded_count(self) -> int:
        """Get count of loaded services"""
        return sum(1 for info in self.services.values() if info['loaded'])
    
    def get_failed_count(self) -> int:
        """Get count of failed services"""
        return sum(1 for info in self.services.values() if not info['loaded'])
