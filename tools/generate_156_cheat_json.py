#!/usr/bin/env python3
"""
GoldHEN Cheat JSON Validator & Generator for GTA V (CUSA00411_01.56)
"""

import json
import sys
from pathlib import Path

CHEATS_FILE = Path(__file__).resolve().parent.parent / "cheats" / "CUSA00411_01.56.json"

def validate_cheat_json(filepath):
    print(f"[*] Validating GoldHEN Cheat JSON at: {filepath}")
    if not filepath.exists():
        print(f"[-] File does not exist: {filepath}")
        return False

    try:
        with open(filepath, "r", encoding="utf-8") as f:
            data = json.load(f)
    except Exception as e:
        print(f"[-] Invalid JSON syntax: {e}")
        return False

    required_keys = ["name", "id", "version", "process", "mods"]
    for key in required_keys:
        if key not in data:
            print(f"[-] Missing required top-level key: {key}")
            return False

    if data["id"] != "CUSA00411":
        print(f"[!] Warning: Title ID is {data['id']}, expected CUSA00411")
    if data["version"] != "01.56":
        print(f"[!] Warning: Version is {data['version']}, expected 01.56")

    mods = data.get("mods", [])
    print(f"[+] Found {len(mods)} cheat modules:")
    for idx, mod in enumerate(mods, 1):
        mod_name = mod.get("name", "Unnamed")
        mem_entries = mod.get("memory", [])
        print(f"    {idx}. {mod_name} ({len(mem_entries)} memory writes)")
        for entry in mem_entries:
            offset = entry.get("offset")
            on_val = entry.get("on")
            off_val = entry.get("off")
            if not offset or not on_val or not off_val:
                print(f"       [-] Corrupt memory entry in {mod_name}: {entry}")
                return False
            # Check hex formatting
            if not offset.startswith("0x"):
                print(f"       [!] Offset should start with 0x: {offset}")
    
    print("[+] JSON structure complies with GoldHEN Cheat Manager specifications!")
    return True

if __name__ == "__main__":
    success = validate_cheat_json(CHEATS_FILE)
    sys.exit(0 if success else 1)
