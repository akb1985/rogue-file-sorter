import logging
from logging.handlers import RotatingFileHandler
import os

def get_logger(name="RogueSorter"):
    logger = logging.getLogger(name)
    if not logger.handlers:
        logger.setLevel(logging.INFO)
        if os.name == 'nt':
            log_dir = os.path.join(os.environ.get('PROGRAMDATA', 'C:\\ProgramData'), 'RogueFileSorter', 'logs')
        else:
            # Per-user log directory
            log_dir = os.path.expanduser('~/.roguefilesorter/logs')
                
        os.makedirs(log_dir, exist_ok=True)
        log_file = os.path.join(log_dir, 'sorter.log')
        
        handler = RotatingFileHandler(log_file, maxBytes=5*1024*1024, backupCount=3)
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        
        console = logging.StreamHandler()
        console.setFormatter(formatter)
        logger.addHandler(console)
        
    return logger