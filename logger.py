"""
Logging utility for better debugging and tracking
"""
import logging
import sys
from pathlib import Path
from datetime import datetime
from config import LOG_FOLDER

def setup_logger(name:  str, log_file: str = None, level=logging.INFO):
    """Setup logger with file and console handlers"""
    
    # Create logs folder if not exists
    LOG_FOLDER.mkdir(exist_ok=True)
    
    # Create logger
    logger = logging.getLogger(name)
    logger.setLevel(level)
    
    # Avoid duplicate handlers
    if logger.handlers:
        return logger
    
    # Format
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    # Console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(level)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
    
    # File handler
    if log_file is None:
        log_file = f"{name}_{datetime.now().strftime('%Y%m%d')}.log"
    
    file_handler = logging.FileHandler(
        LOG_FOLDER / log_file,
        encoding='utf-8'
    )
    file_handler.setLevel(level)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    
    return logger