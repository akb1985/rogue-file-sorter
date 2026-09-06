import os
from typing import Optional, Dict

class ExtensionResolver:
    def __init__(self, mapping: Dict[str, str]):
        self.mapping = {k.lower(): v for k, v in mapping.items()}
        self.ignore_list = {'.crdownload', '.part', '.tmp', '.download'}

    def get_destination(self, filename: str) -> Optional[str]:
        _, ext = os.path.splitext(filename)
        ext = ext.lower()
        if ext in self.ignore_list or not ext:
            return None
        return self.mapping.get(ext)