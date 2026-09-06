import os
import time
from src.logger.log_setup import get_logger

logger = get_logger()

def wait_for_file_ready(filepath: str, timeout: int = 60) -> bool:
    start_time = time.time()
    previous_size = -1
    
    while (time.time() - start_time) < timeout:
        if not os.path.exists(filepath):
            return False 
            
        try:
            current_size = os.path.getsize(filepath)
            if current_size == previous_size and current_size > 0:
                try:
                    with open(filepath, 'rb') as f:
                        f.read(1)
                    return True
                except (IOError, PermissionError):
                    pass
            previous_size = current_size
        except OSError:
            pass
            
        time.sleep(1) 
        
    logger.warning(f"Timeout waiting for file to be ready: {filepath}")
    return False