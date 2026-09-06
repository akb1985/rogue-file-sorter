# Architectural Decisions Log

## 1. Idle Optimization
Implemented dual-mode watcher. Active mode uses `watchdog`. After 10 minutes of inactivity, watchdog observer shuts down. A supervisor loop falls back to polling `os.stat().st_mtime` every 5 seconds (virtually zero CPU cost).

## 2. Race Condition Handling
Instead of relying on OS-level exclusive write locks (which differ across OSs), the engine polls file size. If size is > 0, remains unchanged for 1 full second, and can be opened for a byte read, it is deemed ready.

## 3. Configuration 
Config is copied to a global directory (`ProgramData` or `/etc`) upon installation. Installers do not parse YAML to avoid text corruption; users edit this file directly post-installation.