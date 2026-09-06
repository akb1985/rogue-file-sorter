#!/bin/bash
echo "Building Debian (.deb) package..."
mkdir -p build_deb/DEBIAN
mkdir -p build_deb/usr/local/bin
mkdir -p build_deb/usr/share/roguefilesorter
mkdir -p build_deb/usr/lib/systemd/user

cat <<EOF > build_deb/DEBIAN/control
Package: roguefilesorter
Version: 1.0.0
Architecture: amd64
Maintainer: OpenSource <admin@example.com>
Description: Automatically sorts files based on extensions.
EOF

cp postinst build_deb/DEBIAN/
chmod 755 build_deb/DEBIAN/postinst

cp ../../dist/roguefilesorter build_deb/usr/local/bin/
cp ../../src/config/default_config.yaml build_deb/usr/share/roguefilesorter/
cp roguefilesorter.service build_deb/usr/lib/systemd/user/

dpkg-deb --build build_deb roguefilesorter_1.0.0_amd64.deb
echo "Done. .deb generated."