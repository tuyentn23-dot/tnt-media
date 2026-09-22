"""Centralized Logging System for TNT Media"""
import logging
import os
from logging.handlers import RotatingFileHandler, TimedRotatingFileHandler
from datetime import datetime
from typing import Optional


class TNTLogger:
    """
    Centralized logging for TNT Media.
    Features:
    - Rotating file handlers
    - Console output
    - Structured format
    - Multiple log levels
    """
    
    _instance: Optional['TNTLogger'] = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance
    
    def __init__(self, log_dir: str = "logs", log_level: str = "INFO"):
        if self._initialized:
            return
        
        self.log_dir = log_dir
        self.log_level = getattr(logging, log_level.upper(), logging.INFO)
        self.loggers = {}
        
        os.makedirs(log_dir, exist_ok=True)
        
        self._setup_root_logger()
        self._initialized = True
    
    def _setup_root_logger(self):
        """Setup root logger with handlers"""
        self.root_logger = logging.getLogger("tnt_media")
        self.root_logger.setLevel(self.log_level)
        
        # Clear existing handlers
        self.root_logger.handlers.clear()
        
        # Console handler
        console_handler = logging.StreamHandler()
        console_handler.setLevel(self.log_level)
        console_format = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        console_handler.setFormatter(console_format)
        self.root_logger.addHandler(console_handler)
        
        # File handler - rotating daily
        file_handler = TimedRotatingFileHandler(
            filename=os.path.join(self.log_dir, "tnt_media.log"),
            when="midnight",
            interval=1,
            backupCount=30,
            encoding='utf-8'
        )
        file_handler.setLevel(self.log_level)
        file_format = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        file_handler.setFormatter(file_format)
        self.root_logger.addHandler(file_handler)
        
        # Error file handler
        error_handler = TimedRotatingFileHandler(
            filename=os.path.join(self.log_dir, "error.log"),
            when="midnight",
            interval=1,
            backupCount=30,
            encoding='utf-8'
        )
        error_handler.setLevel(logging.ERROR)
        error_format = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        error_handler.setFormatter(error_format)
        self.root_logger.addHandler(error_handler)
    
    def get_logger(self, name: str) -> logging.Logger:
        """Get a logger for a specific component"""
        if name not in self.loggers:
            logger = logging.getLogger(f"tnt_media.{name}")
            self.loggers[name] = logger
        return self.loggers[name]
    
    def log_event(self, event_type: str, message: str, level: str = "info", **kwargs):
        """Log a structured event"""
        logger = self.get_logger("events")
        
        event_data = {
            "event_type": event_type,
            "message": message,
            "timestamp": datetime.now().isoformat(),
            **kwargs
        }
        
        log_method = getattr(logger, level.lower(), logger.info)
        log_method(f"{event_type}: {message}")
        
        # Also write to event log
        event_log_path = os.path.join(self.log_dir, "events.log")
        with open(event_log_path, 'a', encoding='utf-8') as f:
            import json
            f.write(json.dumps(event_data, ensure_ascii=False) + "\n")
    
    def log_error(self, error: Exception, context: str = ""):
        """Log an error with context"""
        logger = self.get_logger("errors")
        logger.error(f"{context}: {str(error)}", exc_info=True)
    
    def log_performance(self, metric_name: str, value: float, **kwargs):
        """Log a performance metric"""
        self.log_event(
            "performance",
            f"{metric_name}: {value}",
            level="info",
            metric=metric_name,
            value=value,
            **kwargs
        )
    
    def log_content_event(self, content_id: str, event: str, **kwargs):
        """Log a content-related event"""
        self.log_event(
            "content",
            event,
            content_id=content_id,
            **kwargs
        )
    
    def log_channel_event(self, channel_id: str, event: str, **kwargs):
        """Log a channel-related event"""
        self.log_event(
            "channel",
            event,
            channel_id=channel_id,
            **kwargs
        )
    
    def log_campaign_event(self, campaign_id: str, event: str, **kwargs):
        """Log a campaign-related event"""
        self.log_event(
            "campaign",
            event,
            campaign_id=campaign_id,
            **kwargs
        )


# Singleton instance
logger = TNTLogger()
