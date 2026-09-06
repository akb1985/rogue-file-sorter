import sys
from src.logger.log_setup import get_logger

try:
    import win32serviceutil
    import win32service
    import win32event
    import servicemanager
except ImportError:
    win32serviceutil = None

logger = get_logger()

if win32serviceutil:
    class RogueFileSorterService(win32serviceutil.ServiceFramework):
        _svc_name_ = "RogueFileSorter"
        _svc_display_name_ = "Rogue File Auto-Sorter"
        _svc_description_ = "Automatically sorts files into designated folders based on extensions."

        def __init__(self, args):
            win32serviceutil.ServiceFramework.__init__(self, args)
            self.hWaitStop = win32event.CreateEvent(None, 0, 0, None)
            from src.config.config_loader import ConfigManager
            from src.watcher.folder_watcher import WatcherManager
            self.manager = WatcherManager(ConfigManager())

        def SvcStop(self):
            self.ReportServiceStatus(win32service.SERVICE_STOP_PENDING)
            win32event.SetEvent(self.hWaitStop)
            self.manager.stop()

        def SvcDoRun(self):
            servicemanager.LogMsg(
                servicemanager.EVENTLOG_INFORMATION_TYPE,
                servicemanager.PYS_SERVICE_STARTED,
                (self._svc_name_, '')
            )
            logger.info("Windows Service Started")
            
            import threading
            t = threading.Thread(target=self.manager.start)
            t.start()
            
            win32event.WaitForSingleObject(self.hWaitStop, win32event.INFINITE)
            logger.info("Windows Service Stopped")
else:
    class RogueFileSorterService:
        pass