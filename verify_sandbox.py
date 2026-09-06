import os
import time
import tempfile
import threading
from src.config.config_loader import ConfigManager
from src.watcher.folder_watcher import WatcherManager

def run_sandbox_test():
    print("🧪 Starting Sandbox Integration Test...")
    sandbox_dir = tempfile.mkdtemp(prefix="rogue_sandbox_")
    watch_folder = os.path.join(sandbox_dir, "Downloads")
    dest_folder = os.path.join(sandbox_dir, "Documents", "PDFs")
    os.makedirs(watch_folder, exist_ok=True)
    os.makedirs(dest_folder, exist_ok=True)
    
    class MockConfigManager(ConfigManager):
        def __init__(self):
            self.config = {
                "watch_folders": [watch_folder],
                "extension_mapping": {".pdf": dest_folder}
            }
            
    manager = WatcherManager(MockConfigManager())
    t = threading.Thread(target=manager.start, daemon=True)
    t.start()
    
    print(f"👁️  Watching folder: {watch_folder}")
    time.sleep(1)
    
    test_file = os.path.join(watch_folder, "test_report.pdf")
    print(f"📝 Simulating file download: {test_file}")
    with open(test_file, 'w') as f:
        f.write("Fake PDF Content")
        
    print("⏳ Waiting for race-condition lock check and sorting (approx 2s)...")
    time.sleep(3) 
    
    expected_dest = os.path.join(dest_folder, "test_report.pdf")
    if os.path.exists(expected_dest) and not os.path.exists(test_file):
        print("✅ SUCCESS: File was successfully detected and sorted!")
    else:
        print("❌ FAILED: File was not moved to the correct destination.")
        
    manager.stop()
    t.join(timeout=2)
    print("🧹 Sandbox cleanup complete.")

if __name__ == "__main__":
    run_sandbox_test()