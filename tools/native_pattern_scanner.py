#!/usr/bin/env python3
"""
GTA V AOB Pattern Formatter & Native Cross-Map Helper
Converts IDA-style signatures to C++ string / mask format and validates native hash crossmaps.
"""

import sys
import json
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

def ida_pattern_to_code(ida_pattern_str):
    """
    Converts '48 8B 05 ?? ?? ?? ?? 48 85 C0' to:
    Pattern: \x48\x8B\x05\x00\x00\x00\x00\x48\x85\xC0
    Mask:    xxx????xxx
    """
    tokens = ida_pattern_str.strip().split()
    pattern_bytes = []
    mask = []

    for t in tokens:
        if t in ("?", "??"):
            pattern_bytes.append("\\x00")
            mask.append("?")
        else:
            pattern_bytes.append(f"\\x{t.upper()}")
            mask.append("x")

    code_pattern = "".join(pattern_bytes)
    code_mask = "".join(mask)
    return code_pattern, code_mask

def inspect_memory_offsets():
    offsets_file = BASE_DIR / "cheats" / "memory_offsets_156.json"
    if not offsets_file.exists():
        print(f"[-] Offsets file not found: {offsets_file}")
        return

    with open(offsets_file, "r", encoding="utf-8") as f:
        data = json.load(f)

    print("=== GTA V v1.56 AOB Pattern Inspection ===")
    print(f"Target: {data.get('title_id')} @ {data.get('app_version')}\n")

    pointers = data.get("pointers", {})
    for key, pinfo in pointers.items():
        name = pinfo.get("name")
        raw_pattern = pinfo.get("pattern")
        c_pat, c_mask = ida_pattern_to_code(raw_pattern)
        print(f"[*] {name} ({key}):")
        print(f"    IDA Signature: {raw_pattern}")
        print(f"    C++ Pattern:   \"{c_pat}\"")
        print(f"    Mask:          \"{c_mask}\"")
        print(f"    RIP Offset:    +{pinfo.get('rip_offset')} (Len: {pinfo.get('instruction_len')})\n")

if __name__ == "__main__":
    inspect_memory_offsets()
