import time
import os
import threading
from queue import Queue, Empty
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from src.logger.log_setup import get_logger
from src.watcher.race_condition import wait_for_file_ready
from src.sorter.file_mover import FileMover
from src.sorter.extension_map import ExtensionResolver

logger = get_logger()

class SorterEventHandler(FileSystemEventHandler):
    def __init__(self, queue: Queue):
        self.queue = queue

    def on_created(self, event):
        if not event.is_directory: self.queue.put(event.src_path)

    def on_modified(self, event):
        if not event.is_directory: self.queue.put(event.src_path)
            
    def on_moved(self, event):
        if not event.is_directory: self.queue.put(event.dest_path)


class WatcherManager:
    def __init__(self, config_manager):
        self.config = config_manager
        self.resolver = ExtensionResolver(self.config.get_mapping())
        self.folders = self.config.get_watch_folders()
        self.queue = Queue()
        self.observer = None
        self.worker_thread = None
        self._stop_event = threading.Event()
        self.last_activity = time.time()
        self.is_idle = False
        self.idle_timeout = 600
        self.dir_mtimes = {}

    def start(self):
        self._stop_event.clear()
        for folder in self.folders:
            os.makedirs(folder, exist_ok=True)
            self.dir_mtimes[folder] = os.stat(folder).st_mtime
            
        self.worker_thread = threading.Thread(target=self._process_queue, daemon=True)
        self.worker_thread.start()
        self._start_observer()
        self._run_supervisor_loop()

    def _start_observer(self):
        self.observer = Observer()
        handler = SorterEventHandler(self.queue)
        for folder in self.folders:
            self.observer.schedule(handler, folder, recursive=False)
        self.observer.start()
        self.is_idle = False
        logger.info("Watchdog observer active.")

    def _stop_observer(self):
        if self.observer:
            self.observer.stop()
            self.observer.join()
            self.observer = None
        self.is_idle = True
        logger.info("Service entered minimal CPU idle mode.")

    def _run_supervisor_loop(self):
        while not self._stop_event.is_set():
            if not self.is_idle:
                if time.time() - self.last_activity > self.idle_timeout:
                    self._stop_observer()
            else:
                if self._check_for_folder_changes():
                    logger.info("Activity detected. Resuming active monitoring.")
                    self.last_activity = time.time()
                    self._start_observer()
            time.sleep(5 if self.is_idle else 1)

    def _check_for_folder_changes(self) -> bool:
        changed = False
        for folder in self.folders:
            try:
                current_mtime = os.stat(folder).st_mtime
                if current_mtime != self.dir_mtimes.get(folder):
                    self.dir_mtimes[folder] = current_mtime
                    changed = True
                    for f in os.listdir(folder):
                        self.queue.put(os.path.join(folder, f))
            except OSError:
                pass
        return changed

    def _process_queue(self):
        while not self._stop_event.is_set():
            try:
                filepath = self.queue.get(timeout=1)
                self.last_activity = time.time()
                
                # 1. Get the relative folder name (e.g. "PDFs")
                relative_dest = self.resolver.get_destination(os.path.basename(filepath))
                
                if relative_dest:
                    # 2. Construct the destination path based on where the file currently is
                    source_dir = os.path.dirname(filepath)
                    dest_dir = os.path.join(source_dir, relative_dest)
                    
                    if wait_for_file_ready(filepath):
                        FileMover.move(filepath, dest_dir)
                        
                self.queue.task_done()
            except Empty:
                continue
            except Exception as e:
                logger.error(f"Error processing file: {e}")

    def stop(self):
        logger.info("Stopping WatcherManager...")
        self._stop_event.set()
        if self.observer:
            self.observer.stop()
            self.observer.join()
        if self.worker_thread:
            self.worker_thread.join()