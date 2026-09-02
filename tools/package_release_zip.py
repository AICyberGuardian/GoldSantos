#!/usr/bin/env python3
"""
GoldSantos Release Packaging Utility
Packages all verified 1.56 patches, cheats, AFR configs, and documentation into a
clean, ready-to-deploy distribution zip mirroring the PS4 /data/GoldHEN/ filesystem.
"""

import os
import sys
import zipfile
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DIST_DIR = BASE_DIR / "dist"
RELEASE_ZIP = DIST_DIR / "GoldSantos-v1.56-PS4.zip"

def create_release_package():
    print("=== Packaging GoldSantos v1.56 Release Bundle ===")
    DIST_DIR.mkdir(parents=True, exist_ok=True)

    with zipfile.ZipFile(RELEASE_ZIP, "w", zipfile.ZIP_DEFLATED) as zf:
        # 1. Layer 1: XML Game Patches
        patch_file = BASE_DIR / "patches" / "GrandTheftAutoV-Orbis.xml"
        if patch_file.exists():
            arcname = "data/GoldHEN/patches/xml/GrandTheftAutoV-Orbis.xml"
            zf.write(patch_file, arcname)
            print(f"  [+] Added: {arcname}")

        # 2. Layer 2: GoldHEN Cheat JSON
        cheat_file = BASE_DIR / "cheats" / "CUSA00411_01.56.json"
        if cheat_file.exists():
            arcname = "data/GoldHEN/cheats/json/CUSA00411_01.56.json"
            zf.write(cheat_file, arcname)
            print(f"  [+] Added: {arcname}")

        # 3. Layer 3: AFR Source Assets & Meta
        afr_src_dir = BASE_DIR / "afr" / "src"
        for p in afr_src_dir.rglob("*"):
            if p.is_file():
                rel_p = p.relative_to(afr_src_dir)
                arcname = f"data/GoldHEN/AFR/CUSA00411/src/{rel_p.as_posix()}"
                zf.write(p, arcname)
                print(f"  [+] Added: {arcname}")

        # 4. Plugins Configuration Snippet
        plugins_ini_content = """# GoldSantos GTA V v1.56 Plugin Configuration
# Place in /data/GoldHEN/plugins.ini

[CUSA00411]
/data/GoldHEN/plugins/afr.prx=true
# /data/GoldHEN/plugins/gtav_menu_156.prx=true
"""
        zf.writestr("data/GoldHEN/plugins.ini.example", plugins_ini_content)
        print("  [+] Added: data/GoldHEN/plugins.ini.example")

        # 5. Core Docs & Quickstart
        readme_file = BASE_DIR / "README.md"
        if readme_file.exists():
            zf.write(readme_file, "README.md")
            print("  [+] Added: README.md")

        license_file = BASE_DIR / "LICENSE"
        if license_file.exists():
            zf.write(license_file, "LICENSE")
            print("  [+] Added: LICENSE")

    zip_size_kb = RELEASE_ZIP.stat().st_size / 1024
    print(f"\n[+] Distribution bundle successfully created!")
    print(f"[*] Path: {RELEASE_ZIP} ({zip_size_kb:.2f} KB)")
    print("[*] Ready for GitHub Releases and USB / FTP deployment.")

if __name__ == "__main__":
    create_release_package()
