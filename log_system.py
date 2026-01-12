# --- log_system.py ---
import logging
from logging.handlers import RotatingFileHandler

def setup_logger():
    logger = logging.getLogger("game_logger")
    logger.setLevel(logging.DEBUG)

    # Handlers
    f_handler = RotatingFileHandler("game_log.log", maxBytes=2000)
    c_handler = logging.StreamHandler()
    
    format_str = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    f_handler.setFormatter(format_str)
    c_handler.setFormatter(format_str)

    logger.addHandler(f_handler)
    logger.addHandler(c_handler)
    return logger

# Initialize it HERE so it's ready upon import
log = setup_logger()