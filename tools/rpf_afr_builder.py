#!/usr/bin/env python3
"""
GoldHEN AFR Directory Stager & Verification Utility
Prepares, validates, and inspects assets destined for /data/GoldHEN/AFR/CUSA00411/update/update.rpf
Supports automated packaging via rpf-cli (Rust) or OpenIV.
"""

import os
import sys
import shutil
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
AFR_DIR = BASE_DIR / "afr"
SRC_DIR = AFR_DIR / "src"
DEST_DIR = AFR_DIR / "CUSA00411" / "update"

def check_staged_assets():
    print("=== GoldHEN AFR Workspace Status ===")
    print(f"[*] Base Source Directory: {SRC_DIR}")
    print(f"[*] Destination Directory: {DEST_DIR}")

    DEST_DIR.mkdir(parents=True, exist_ok=True)
    
    # Check source modifications
    handling_file = SRC_DIR / "handling" / "handling_chaos_boost.meta"
    visual_file = SRC_DIR / "visualsettings" / "visualsettings_clean.dat"
    timecycle_file = SRC_DIR / "timecycle" / "timecycle_mods_clean.xml"
    decal_meta = SRC_DIR / "decals" / "peddamagedecals_config.meta"
    decal_notes = SRC_DIR / "decals" / "peddamagedecals_notes.md"

    print("\n[Source Assets Available for Packaging]:")
    print(f"  - Handling Meta:      {'[OK]' if handling_file.exists() else '[MISSING]'} ({handling_file.name})")
    print(f"  - Visual Settings:    {'[OK]' if visual_file.exists() else '[MISSING]'} ({visual_file.name})")
    print(f"  - Timecycle Clear:    {'[OK]' if timecycle_file.exists() else '[MISSING]'} ({timecycle_file.name})")
    print(f"  - Decals Config Meta: {'[OK]' if decal_meta.exists() else '[MISSING]'} ({decal_meta.name})")
    print(f"  - Decals Guide:       {'[OK]' if decal_notes.exists() else '[MISSING]'} ({decal_notes.name})")

    # Check for rpf-cli tool in PATH
    rpf_cli_bin = shutil.which("rpf-cli")
    print("\n[Archive Tooling Detection]:")
    if rpf_cli_bin:
        print(f"  [+] rpf-cli found in PATH: {rpf_cli_bin}")
        print("  [+] Automated headless RPF packaging is ready!")
    else:
        print("  [i] rpf-cli not found in system PATH.")
        print("      Install via Cargo: cargo install rpf-cli (or use Windows OpenIV GUI)")

    rpf_target = DEST_DIR / "update.rpf"
    print("\n[Staged Target Archive]:")
    if rpf_target.exists():
        size_mb = rpf_target.stat().st_size / (1024 * 1024)
        print(f"  [+] Staged update.rpf present: {size_mb:.2f} MB")
        print("  [+] Ready for LAN deployment via tools/deploy_mod_stack_lan.py --afr")
    else:
        print("  [i] No update.rpf currently in destination.")
        print("  [i] Packaging instructions:")
        print("      1. Extract clean PS4 update.rpf (using OpenIV or rpf-cli extract)")
        print("      2. Copy afr/src/ assets into extracted common/ and x64/ paths")
        print("      3. Repack to: afr/CUSA00411/update/update.rpf")

if __name__ == "__main__":
    check_staged_assets()
