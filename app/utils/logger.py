"""
Logging configuration for the chatbot API.
Creates a structured logger that writes to chatbot.log file.
"""

import logging
import sys
from pathlib import Path
from typing import Optional

# Project root directory
PROJECT_ROOT = Path(__file__).parent.parent.parent
LOG_FILE = PROJECT_ROOT / "chatbot.log"


def setup_logger(name: str = "chatbot", log_file: Optional[Path] = None, level: int = logging.INFO) -> logging.Logger:
    """
    Set up a structured logger with file and console handlers.
    
    Args:
        name: Logger name
        log_file: Path to log file (defaults to chatbot.log in project root)
        level: Logging level
        
    Returns:
        Configured logger instance
    """
    if log_file is None:
        log_file = LOG_FILE
    
    # Create logger
    logger = logging.getLogger(name)
    logger.setLevel(level)
    
    # Avoid duplicate handlers if logger already configured
    if logger.handlers:
        return logger
    
    # Create formatter: timestamp - level - message
    formatter = logging.Formatter(
        fmt="%(asctime)s - %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )
    
    # File handler - write to chatbot.log
    file_handler = logging.FileHandler(log_file, encoding="utf-8")
    file_handler.setLevel(level)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    
    # Console handler - also print to stdout
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(level)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
    
    return logger


# Global logger instance
_logger: Optional[logging.Logger] = None


def get_logger() -> logging.Logger:
    """Get or create the global logger instance."""
    global _logger
    if _logger is None:
        _logger = setup_logger()
    return _logger

