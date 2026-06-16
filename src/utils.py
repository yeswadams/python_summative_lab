import logging
import os

def setup_logging(log_file: str = "app.log"):
    """Configures the standard logging utility."""
    # Get the directory of the current file (src/) and go up one level to the project root
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    log_path = os.path.join(base_dir, log_file)
    
    logger = logging.getLogger("PM-CLI")
    logger.setLevel(logging.DEBUG)
    
    if not logger.handlers:
        fh = logging.FileHandler(log_path, mode='a', encoding='utf-8')
        fh.setLevel(logging.DEBUG)
        fh_formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
        fh.setFormatter(fh_formatter)
        
        ch = logging.StreamHandler()
        ch.setLevel(logging.WARNING)
        ch_formatter = logging.Formatter("[%(levelname)s] %(message)s")
        ch.setFormatter(ch_formatter)
        
        logger.addHandler(fh)
        logger.addHandler(ch)
    
    return logger

logger = setup_logging()

def validate_non_empty(value: str, field_name: str):
    """Simple validator to ensure strings are not empty or just whitespace."""
    if not value or not value.strip():
        raise ValueError(f"{field_name} cannot be empty.")
    return value.strip()
