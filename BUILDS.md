# Build Instructions

## Prerequisites
1. Python 3.11+
2. Required packages: `pip install -r requirements.txt`
3. Platform Tools:
   - **Windows:** WiX Toolset v3 (ensure `candle.exe` and `light.exe` are in PATH).
   - **macOS:** Xcode Command Line Tools.
   - **Linux:** `dpkg-deb` installed.

## Running the Build
Run this from the project root:
```bash
chmod +x build/build_all.sh
./build/build_all.sh