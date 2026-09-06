import signal
import sys
import time
from src.logger.log_setup import get_logger
from src.config.config_loader import ConfigManager
from src.watcher.folder_watcher import WatcherManager

logger = get_logger()

class UnixDaemon:
    def __init__(self):
        self.manager = WatcherManager(ConfigManager())
        
    def _signal_handler(self, signum, frame):
        logger.info(f"Received signal {signum}. Shutting down...")
        self.manager.stop()
        sys.exit(0)

    def run(self):
        signal.signal(signal.SIGINT, self._signal_handler)
        signal.signal(signal.SIGTERM, self._signal_handler)
        
        logger.info("Starting Unix Daemon loop...")
        self.manager.start()
        
        while True:
            time.sleep(1)