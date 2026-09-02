#!/usr/bin/env python3
"""
GoldHEN AFR Directory Stager & Verification Utility
Prepares and inspects assets destined for /data/GoldHEN/AFR/CUSA00411/update/update.rpf
"""

import os
import sys
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
    decal_notes = SRC_DIR / "decals" / "peddamagedecals_notes.md"

    print("\n[Source Assets Available for Packaging]:")
    print(f"  - Handling Meta: {'[OK]' if handling_file.exists() else '[MISSING]'} ({handling_file.name})")
    print(f"  - Visual Settings: {'[OK]' if visual_file.exists() else '[MISSING]'} ({visual_file.name})")
    print(f"  - Decals Guide: {'[OK]' if decal_notes.exists() else '[MISSING]'} ({decal_notes.name})")

    rpf_target = DEST_DIR / "update.rpf"
    print("\n[Staged Target Archive]:")
    if rpf_target.exists():
        size_mb = rpf_target.stat().st_size / (1024 * 1024)
        print(f"  [+] Staged update.rpf present: {size_mb:.2f} MB")
        print("  [+] Ready for LAN deployment via deploy_mod_stack_lan.py --afr")
    else:
        print("  [i] No update.rpf currently in destination.")
        print("  [i] Build your custom update.rpf using OpenIV/rpftool with source assets,")
        print(f"      then place it at: {rpf_target}")

if __name__ == "__main__":
    check_staged_assets()
