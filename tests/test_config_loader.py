import os
import yaml
import tempfile
from src.config.config_loader import ConfigManager

def test_config_loader_expand_user():
    fd, path = tempfile.mkstemp()
    test_config = {
        "watch_folders": ["~/Downloads"],
        "extension_mapping": {".txt": "~/Docs"}
    }
    with os.fdopen(fd, 'w') as f:
        yaml.dump(test_config, f)
        
    cm = ConfigManager(config_path=path)
    
    assert "~" not in cm.get_watch_folders()[0]
    assert cm.get_watch_folders()[0] == os.path.expanduser("~/Downloads")
    assert cm.get_mapping()[".txt"] == os.path.expanduser("~/Docs")
    
    os.remove(path)