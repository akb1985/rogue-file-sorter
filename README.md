# Rogue File Auto-Sorter

A cross-platform, zero-configuration background service that watches your download folders and automatically sorts files into designated directories based on their extensions.

## Features
- **True Background Daemon:** Runs natively as a Windows Service, macOS launchd daemon, or Linux systemd unit.
- **Eco-Friendly:** Consumes <0.1% CPU when idle. 
- **Safe:** Prevents "silent overwrites" by auto-incrementing filenames.

## Installation
- **Windows:** Download `.msi` and run.
- **macOS:** Download `.pkg` and run.
- **Linux:** Download `.deb` and run `sudo apt install ./roguefilesorter*.deb`

## Configuration
Edit the global configuration file to add custom watch folders or mappings. Restart the service to apply changes.
- **Windows:** `C:\ProgramData\RogueFileSorter\config.yaml`
- **macOS/Linux:** `/etc/roguefilesorter/config.yaml`

## Architecture
See DECISIONS.md for architectural details.

## Building
See BUILDS.md for build instructions.