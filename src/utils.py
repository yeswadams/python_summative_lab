import logging
import os

def setup_logging(log_file: str = "app.log"):
    """Configures the standard logging utility."""
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        handlers=[
            logging.FileHandler(log_file),
            logging.StreamHandler()
        ]
    )
    return logging.getLogger("PM-CLI")

logger = setup_logging()

def validate_non_empty(value: str, field_name: str):
    """Simple validator to ensure strings are not empty or just whitespace."""
    if not value or not value.strip():
        raise ValueError(f"{field_name} cannot be empty.")
    return value.strip()
