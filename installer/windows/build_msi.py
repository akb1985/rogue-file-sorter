import os
import sys
import urllib.request
import zipfile
import subprocess
from pathlib import Path

# URLs and Paths
WIX_VERSION = "wix3112rtm"
WIX_ZIP_URL = f"https://github.com/wixtoolset/wix3/releases/download/{WIX_VERSION}/wix311-binaries.zip"

# Resolve absolute paths relative to this script
SCRIPT_DIR = Path(__file__).parent.resolve()
TOOLS_DIR = SCRIPT_DIR / ".tools" / "wix"
WIX_ZIP_PATH = TOOLS_DIR / "wix-binaries.zip"

CANDLE_EXE = TOOLS_DIR / "candle.exe"
LIGHT_EXE = TOOLS_DIR / "light.exe"

def download_and_extract_wix():
    """Downloads and extracts WiX toolset locally so the developer doesn't have to install it."""
    if CANDLE_EXE.exists() and LIGHT_EXE.exists():
        print("✅ WiX Toolset is already available locally.")
        return

    print(f"⬇️  Downloading WiX Toolset portable binaries from GitHub...")
    TOOLS_DIR.mkdir(parents=True, exist_ok=True)
    
    try:
        # Download the zip
        urllib.request.urlretrieve(WIX_ZIP_URL, WIX_ZIP_PATH)
        print("📦 Extracting WiX binaries...")
        
        # Extract the zip
        with zipfile.ZipFile(WIX_ZIP_PATH, 'r') as zip_ref:
            zip_ref.extractall(TOOLS_DIR)
            
        # Cleanup zip file
        WIX_ZIP_PATH.unlink()
        print("✅ WiX Toolset downloaded and extracted successfully.")
    except Exception as e:
        print(f"❌ Failed to download/extract WiX: {e}")
        sys.exit(1)

def build_msi():
    """Runs candle.exe and light.exe to build the MSI."""
    print("🔨 Compiling WiX XML (candle.exe)...")
    
    # We use the absolute path to the local candle.exe
    candle_cmd = [
        str(CANDLE_EXE),
        "product.wxs",
        "-out", "product.wixobj"
    ]
    subprocess.run(candle_cmd, cwd=SCRIPT_DIR, check=True)

    print("🔗 Linking MSI (light.exe)...")
    light_cmd = [
        str(LIGHT_EXE),
        "product.wixobj",
        "-ext", "WixUIExtension",
        "-out", "RogueFileSorter.msi"
    ]
    subprocess.run(light_cmd, cwd=SCRIPT_DIR, check=True)
    print("🎉 Success! RogueFileSorter.msi generated in installer/windows/")

if __name__ == "__main__":
    download_and_extract_wix()
    build_msi()