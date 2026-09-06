import os
import sys
import argparse
from src.logger.log_setup import get_logger

logger = get_logger()

def sort_existing_files():
    """Immediately scans watch folders and sorts existing files."""
    from src.config.config_loader import ConfigManager
    from src.sorter.extension_map import ExtensionResolver
    from src.sorter.file_mover import FileMover
    
    config = ConfigManager()
    resolver = ExtensionResolver(config.get_mapping())
    folders = config.get_watch_folders()
    
    logger.info("Starting retroactive sort of existing files...")
    moved_count = 0
    
    for folder in folders:
        if not os.path.exists(folder):
            continue
            
        for filename in os.listdir(folder):
            filepath = os.path.join(folder, filename)
            
            # Skip directories
            if os.path.isdir(filepath):
                continue
                
            relative_dest = resolver.get_destination(filename)
            if relative_dest:
                dest_dir = os.path.join(folder, relative_dest)
                if FileMover.move(filepath, dest_dir):
                    moved_count += 1
                    
    logger.info(f"Retroactive sort complete. Moved {moved_count} files.")
    print(f"✅ Sorting complete! Moved {moved_count} files.")

def run_service():
    if os.name == 'nt':
        try:
            import servicemanager
            import win32serviceutil
            from src.service.windows_service import RogueFileSorterService
            
            if len(sys.argv) == 1:
                servicemanager.Initialize()
                servicemanager.PrepareToHostSingle(RogueFileSorterService)
                servicemanager.StartServiceCtrlDispatcher()
            else:
                win32serviceutil.HandleCommandLine(RogueFileSorterService)
        except ImportError:
            print("win32 modules not installed. Cannot run as Windows Service.")
    else:
        from src.service.unix_service import UnixDaemon
        daemon = UnixDaemon()
        daemon.run()

def main():
    parser = argparse.ArgumentParser(description="Rogue File Sorter Service")
    parser.add_argument('--standalone', action='store_true', help="Run directly in terminal (dev mode)")
    parser.add_argument('--sort-now', action='store_true', help="Instantly sort all existing files in watch folders")
    
    args, unknown = parser.parse_known_args()
    
    if args.sort_now:
        sort_existing_files()
        sys.exit(0)
        
    if args.standalone:
        from src.service.unix_service import UnixDaemon
        daemon = UnixDaemon()
        daemon.run()
    else:
        run_service()

if __name__ == "__main__":
    main()