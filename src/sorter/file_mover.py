import os
import shutil
from src.logger.log_setup import get_logger

logger = get_logger()

class FileMover:
    @staticmethod
    def get_safe_destination(dest_dir: str, filename: str) -> str:
        os.makedirs(dest_dir, exist_ok=True)
        base, ext = os.path.splitext(filename)
        counter = 1
        target_path = os.path.join(dest_dir, filename)
        while os.path.exists(target_path):
            target_path = os.path.join(dest_dir, f"{base} ({counter}){ext}")
            counter += 1
        return target_path

    @staticmethod
    def move(src_path: str, dest_dir: str) -> bool:
        try:
            filename = os.path.basename(src_path)
            safe_dest = FileMover.get_safe_destination(dest_dir, filename)
            shutil.move(src_path, safe_dest)
            logger.info(f"Moved: {filename} -> {safe_dest}")
            return True
        except Exception as e:
            logger.error(f"Failed to move {src_path} to {dest_dir}: {e}")
            return False