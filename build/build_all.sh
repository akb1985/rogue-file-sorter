#!/bin/bash
set -e

echo "========================================"
echo "🚀 Rogue File Sorter - Master Build"
echo "========================================"

cd "$(dirname "$0")/.."
mkdir -p dist/releases

echo "📦 Step 1: Bundling Python code with PyInstaller..."
pyinstaller --noconfirm --onefile --windowed \
    --hidden-import win32timezone \
    --name roguefilesorter \
    run.py

echo "📦 Step 2: Building OS-specific Installer..."
OS_NAME=$(uname -s)

if [[ "$OS_NAME" == "MINGW"* ]] || [[ "$OS_NAME" == "CYGWIN"* ]] || [[ "$OS_NAME" == "MSYS"* ]]; then
    echo "Detected Windows. Triggering automated Python WiX build..."
    cd installer/windows
    python build_msi.py
    mv RogueFileSorter.msi ../../dist/releases/
    echo "✅ Windows MSI built successfully."
elif [[ "$OS_NAME" == "Darwin" ]]; then
    echo "Detected macOS. Triggering pkgbuild..."
    cd installer/macos
    chmod +x build.sh
    ./build.sh
    mv RogueFileSorter.pkg ../../dist/releases/
    echo "✅ macOS PKG built successfully."
elif [[ "$OS_NAME" == "Linux" ]]; then
    echo "Detected Linux. Triggering dpkg-deb build..."
    cd installer/linux
    chmod +x build_deb.sh
    ./build_deb.sh
    mv *.deb ../../dist/releases/
    echo "✅ Linux DEB built successfully."
else
    echo "Unsupported OS for automated packaging: $OS_NAME"
    exit 1
fi
echo "🎉 Build Complete! Artifacts are in dist/releases/"