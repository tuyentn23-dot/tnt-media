"""Configuration Manager for TNT Media"""
import os
import json
import yaml
from typing import Dict, Any, Optional
from dotenv import load_dotenv


class ConfigManager:
    """
    Centralized configuration management.
    Loads from:
    1. Environment variables (.env)
    2. YAML/JSON config files
    3. Default values
    """
    
    _instance: Optional['ConfigManager'] = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance
    
    def __init__(self, config_dir: str = "config"):
        if self._initialized:
            return
        
        self.config_dir = config_dir
        self.config: Dict[str, Any] = {}
        
        # Load .env file
        load_dotenv()
        
        # Load config files
        self._load_config_files()
        
        # Load environment variables
        self._load_env_variables()
        
        self._initialized = True
    
    def _load_config_files(self):
        """Load all config files from config directory"""
        if not os.path.exists(self.config_dir):
            return
        
        for filename in os.listdir(self.config_dir):
            filepath = os.path.join(self.config_dir, filename)
            
            try:
                if filename.endswith('.json'):
                    with open(filepath, 'r', encoding='utf-8') as f:
                        key = filename.replace('.json', '')
                        self.config[key] = json.load(f)
                elif filename.endswith('.yaml') or filename.endswith('.yml'):
                    with open(filepath, 'r', encoding='utf-8') as f:
                        key = filename.replace('.yaml', '').replace('.yml', '')
                        self.config[key] = yaml.safe_load(f)
            except Exception as e:
                print(f"Error loading config {filename}: {e}")
    
    def _load_env_variables(self):
        """Load environment variables"""
        env_vars = {
            "YOUTUBE_API_KEY": os.getenv("YOUTUBE_API_KEY"),
            "YOUTUBE_CLIENT_ID": os.getenv("YOUTUBE_CLIENT_ID"),
            "YOUTUBE_CLIENT_SECRET": os.getenv("YOUTUBE_CLIENT_SECRET"),
            "TIKTOK_API_KEY": os.getenv("TIKTOK_API_KEY"),
            "DATABASE_URL": os.getenv("DATABASE_URL", "sqlite:///tnt_media.db"),
            "API_HOST": os.getenv("API_HOST", "0.0.0.0"),
            "API_PORT": int(os.getenv("API_PORT", "8000")),
            "API_DEBUG": os.getenv("API_DEBUG", "true").lower() == "true",
            "LOG_LEVEL": os.getenv("LOG_LEVEL", "INFO"),
            "AUTO_PUBLISH": os.getenv("AUTO_PUBLISH", "false").lower() == "true",
            "MAX_DAILY_PUBLISH": int(os.getenv("MAX_DAILY_PUBLISH", "3")),
        }
        
        self.config["env"] = env_vars
    
    def get(self, key: str, default: Any = None) -> Any:
        """Get config value by key (dot notation supported)"""
        keys = key.split('.')
        value = self.config
        
        for k in keys:
            if isinstance(value, dict):
                value = value.get(k)
                if value is None:
                    return default
            else:
                return default
        
        return value
    
    def set(self, key: str, value: Any):
        """Set config value"""
        keys = key.split('.')
        target = self.config
        
        for k in keys[:-1]:
            if k not in target:
                target[k] = {}
            target = target[k]
        
        target[keys[-1]] = value
    
    def get_all(self) -> Dict[str, Any]:
        """Get all config"""
        return self.config
    
    def save_config(self, filename: str = "config_snapshot.json"):
        """Save current config to file"""
        filepath = os.path.join(self.config_dir, filename)
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(self.config, f, indent=2, ensure_ascii=False)
        
        return filepath
    
    def validate_required_keys(self, required_keys: list) -> Dict[str, bool]:
        """Validate that required config keys exist"""
        result = {}
        for key in required_keys:
            result[key] = self.get(key) is not None
        return result


# Singleton instance
config = ConfigManager()
