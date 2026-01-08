import logging
from math import log
import os

LOG_DIR = './logs'
LOG_FILE = 'app.log'

# with open(LOG_DIR+"/"+LOG_FILE, "w") as file:
#     file.write("sfsss")
    
def setup_logger(name: str = 'app') -> logging.Logger:
    os.makedirs(LOG_DIR, exist_ok=True)
    
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    
    if logger.handlers:
        return logger
    
    file_handler = logging.FileHandler(
        os.path.join(LOG_DIR, LOG_FILE)
    )
    file_handler.setLevel(logging.DEBUG)
    
    formatter = logging.Formatter(
        "%(asctime)s | %(levelname)s | %(name)s | %(message)s",
        "%Y-%m-%d %H:%M:%S"
    )
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    logger.propagate = False    
    return logger
    