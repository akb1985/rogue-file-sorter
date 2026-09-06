import os
import yaml
import shutil
from typing import Dict, List
from src.logger.log_setup import get_logger

logger = get_logger()

class ConfigManager:
    def __init__(self, config_path: str = None):
        self.config_path = config_path or self._get_default_config_path()
        self.config = self.load_config()

    def _get_default_config_path(self) -> str:
        if os.name == 'nt':
            base = os.environ.get('PROGRAMDATA', 'C:\\ProgramData')
            return os.path.join(base, 'RogueFileSorter', 'config.yaml')
        else:
            # User-specific config directory!
            return os.path.expanduser('~/.config/roguefilesorter/config.yaml')

    def load_config(self) -> dict:
        # Auto-create user config from global template if it doesn't exist
        if not os.path.exists(self.config_path):
            os.makedirs(os.path.dirname(self.config_path), exist_ok=True)
            global_template = '/usr/share/roguefilesorter/default_config.yaml'
            if os.path.exists(global_template):
                shutil.copy(global_template, self.config_path)
            else:
                logger.warning("Global template missing. Using hardcoded defaults.")
                return self._get_fallback_config()
            
        try:
            with open(self.config_path, 'r') as f:
                config = yaml.safe_load(f)
                
            config['watch_folders'] = [os.path.expanduser(p) for p in config.get('watch_folders', [])]
            config['extension_mapping'] = config.get('extension_mapping', {})
            return config
        except Exception as e:
            logger.error(f"Failed to load config from {self.config_path}: {e}")
            return self._get_fallback_config()

    def _get_fallback_config(self) -> dict:
        return {
            "watch_folders": [os.path.expanduser("~/Downloads")],
            "extension_mapping": {".pdf": "PDFs"}
        }
    
    def get_watch_folders(self) -> List[str]:
        return self.config.get("watch_folders", [])

    def get_mapping(self) -> Dict[str, str]:
        return self.config.get("extension_mapping", {})