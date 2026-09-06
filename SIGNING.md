# Code Signing & Distribution Guide

- **Windows:** Distributing unsigned `.msi` triggers SmartScreen. Purchase an EV Code Signing Cert to bypass immediately, or standard OV Cert to build reputation. Workaround: Users click "More Info -> Run anyway".
- **macOS:** Apple Developer Program ($99/yr) is required to sign (`codesign`, `productsign`) and notarize (`notarytool`) the `.pkg`. Workaround: Users Right-Click the package -> Open -> Open anyway to bypass Gatekeeper.
- **Linux:** Sign package repositories via GPG keys. Direct `.deb` downloads bypass major warnings.