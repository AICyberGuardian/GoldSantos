# 🌴 GoldSantos

```text
       ██████╗  ██████╗ ██╗     ██████╗ ███████╗ █████╗ ███╗   ██╗████████╗ ██████╗ ███████╗
      ██╔════╝ ██╔═══██╗██║     ██╔══██╗██╔════╝██╔══██╗████╗  ██║╚══██╔══╝██╔═══██╗██╔════╝
      ██║  ███╗██║   ██║██║     ██║  ██║███████╗███████║██╔██╗ ██║   ██║   ██║   ██║███████╗
      ██║   ██║██║   ██║██║     ██║  ██║╚════██║██╔══██║██║╚██╗██║   ██║   ██║   ██║╚════██║
      ╚██████╔╝╚██████╔╝███████╗██████╔╝███████║██║  ██║██║ ╚████║   ██║   ╚██████╔╝███████║
       ╚═════╝  ╚═════╝ ╚══════╝╚═════╝ ╚══════╝╚═╝  ╚═╝╚═╝  ╚═══╝   ╚═╝    ╚═════╝ ╚══════╝
```

> **The Ultimate Decoupled GTA V (v1.56 / CUSA00411) Modding Suite & Chaos Engine for PlayStation 4 (GoldHEN v2.4b on Firmware 11.02 / 9.00 / 5.05).**

[![PS4 Firmware](https://img.shields.io/badge/PS4%20FW-11.02%20%7C%209.00%20%7C%205.05-blue.svg)](https://github.com/GoldHEN/GoldHEN)
[![GoldHEN](https://img.shields.io/badge/GoldHEN-v2.4b-gold.svg)](https://github.com/GoldHEN/GoldHEN)
[![GTA V Version](https://img.shields.io/badge/GTA%20V-v1.56%20(CUSA00411)-green.svg)](https://github.com/AICyberGuardian/GoldSantos)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

---

## 🎯 Project Mission: Decoupled Architecture

GoldSantos transforms your jailbroken **PS4 (Fat CUH-1001A / Slim / Pro)** into an ultra-high-performance, crash-free GTA V sandbox using a **strictly decoupled design**:
* **100% Stability:** The retail game package (`01 Base`, `02 Update v1.56`, `03 DLC`) remains pristine and unmodified. Zero kernel panics (`CE-34878-0`), zero save corruption, and zero controller R2 trigger glitches.
* **Granular Control:** Every mod tier (engine patches, memory cheats, AFR asset overhauls, and PRX mod menus) can be toggled on or off independently.
* **1-Click Gigabit LAN Deployment:** Push patches, cheats, and configs to `/data/GoldHEN/` over local Ethernet in seconds.

---

## 🔬 Mod Lineage & Technical Reality on v1.56

Rockstar shuffles `eboot.bin` offsets, scrambles native function hashes, and shifts script arrays on every title update.

| Classic Mod | Original Target | Status on 1.56 | Technical Reality & Replacement Lineage |
| :--- | :---: | :---: | :--- |
| **Scorpion** (by `RF0oDxM0Dz`) | 1.48 / 1.50 (v1.2B) | ❌ Incompatible | Stopped at 1.50. Replaced by the same author's **Orbx Engine** (1.56) and **Oxagon Lite** (1.53/1.56). Do not load Scorpion 1.2B on 1.56. |
| **Lotus SPRX** (`0x199` / illusion) | 1.27 / 1.48 | ❌ Incompatible | Supported 1.27/1.48 only. No public 1.56 Lotus `.sprx` exists. |
| **BeefQueef / GoldQueef** | 1.47 / 1.67 | ❌ Incompatible | Dead legacy trainer. Absorbed by modern 1.56 suites. |
| **Lamance / WildeModz** | 1.00 – 1.38 | ❌ Incompatible | Obsolete 2018 WebKit browser `.bin` payloads / old script mods. |
| **God's Blessing 1.56** | 1.56 | ⚠️ Rejected | Pre-patched Franken-PKG with modified executable. Prone to controller glitches and stripped menus (~25 cars). |
| **illusion XML Patches** | 1.56 | ✅ Verified | Official in-memory engine patches: **60 FPS Unlock** (CPU Limited on Fat), **Skip Intro**, and **Snow in SP**. |
| **GoldHEN 1.56 Cheats** | 1.56 | ✅ Verified | Custom memory trainer JSON (`CUSA00411_01.56.json`) for God Mode, Never Wanted, Infinite Ammo, and $2.14B cash via Share button. |

---

## 📂 Repository Layout

```text
GoldSantos/
├── README.md                           # Master Documentation & Architecture Manual
├── LICENSE                             # MIT Open Source License
├── docs/                               # Technical Specifications & Reverse Engineering
│   ├── ARCHITECTURE_AND_CRASH_ANALYSIS.md
│   ├── NATIVE_CROSSMAP_AND_PORTING.md
│   └── SAFE_CHAOS_ROADMAP.md
├── patches/                            # GoldHEN XML In-Memory Game Patches
│   └── GrandTheftAutoV-Orbis.xml       # 60 FPS Unlock, Skip Intro Logos, Snow in SP
├── cheats/                             # GoldHEN Cheat Manager JSON & Pointer Maps
│   ├── CUSA00411_01.56.json            # 11 Verified Memory Cheats (God Mode, Ammo, Cash)
│   └── memory_offsets_156.json         # Mapped Pointers, Offsets & AOB Signatures
├── afr/                                # GoldHEN Application File Redirector (AFR)
│   ├── README.md                       # Monolithic update.rpf Architecture Guide
│   ├── CUSA00411/update/               # Target Destination for Staged update.rpf
│   └── src/                            # Source Assets (Handling, Visualsettings, Decals)
│       ├── handling/handling_chaos_boost.meta
│       ├── visualsettings/visualsettings_clean.dat
│       ├── timecycle/timecycle_mods_clean.xml
│       └── decals/peddamagedecals_config.meta
├── plugins/                            # OpenOrbis & GoldHEN Plugin SDK Pipeline
│   └── lotus-base/                     # Recompiled 1.56-Native Mod Menu Base
│       ├── include/ (crossmap.h, natives_156.h, types.h, menu.h)
│       ├── src/ (main.cpp, menu.cpp, hooks.cpp)
│       └── Makefile                    # OpenOrbis Clang Build Script
└── tools/                              # Automated Management & Deployment Tooling
    ├── deploy_mod_stack_lan.py         # 1-Click LAN FTP Deployer to PS4
    ├── generate_156_cheat_json.py      # Cheat JSON Validator & Builder
    ├── rpf_afr_builder.py              # AFR Workspace Stager & Inspector
    └── native_pattern_scanner.py       # AOB Signature & Cross-Map Helper
```

---

## 🚀 Quick Start & 1-Click Deployment

### 1. Requirements:
* Jailbroken PS4 running **GoldHEN v2.4b+** (HEN 11.02 / 9.00 / 5.05).
* Clean **GTA V v1.56 (`CUSA00411`)** installed.
* Python 3.10+ (or `uv`).

### 2. Deploy Full Mod Stack to PS4 over LAN:
```powershell
# Deploy all verified patches and cheats directly to PS4:
python tools/deploy_mod_stack_lan.py --ip <YOUR_PS4_IP> --all
```

### 3. In-Game Verification:
* **60 FPS & Snow:** Ensure **Plugin Settings $\rightarrow$ Game Patch** is `ON` in GoldHEN. Launch GTA V to see confirmation notification.
* **Real-Time Cheats:** Ensure **Cheat Settings $\rightarrow$ Cheat Menu** is `ON` in GoldHEN. Hold the **Share** button in-game to toggle God Mode, Never Wanted, and Infinite Ammo!

---

## ⚖️ Legal & DMCA Compliance

GoldSantos contains **zero copyrighted game binaries, no PKGs, and no decrypted proprietary assets**. It provides only open-source C++ headers, memory crossmaps, XML patch definitions, JSON trainer specifications, and local automation scripts. All trademarks belong to their respective owners.
