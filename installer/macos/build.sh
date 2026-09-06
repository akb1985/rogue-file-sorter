#!/bin/bash
echo "Building macOS .pkg installer..."
mkdir -p payload/usr/local/bin
mkdir -p payload/tmp/roguefilesorter_payload
mkdir -p scripts

cp ../../dist/roguefilesorter payload/usr/local/bin/
cp ../../src/config/default_config.yaml payload/tmp/roguefilesorter_payload/
cp com.roguefilesorter.daemon.plist payload/tmp/roguefilesorter_payload/
cp postinstall scripts/
chmod +x scripts/postinstall

pkgbuild --root payload --scripts scripts --identifier com.roguefilesorter.app --version 1.0 RogueFileSorter.pkg
echo "Done. PKG generated."