---
name: ps4-gtav-modder
description: Use when configuring, deploying, troubleshooting, or porting mods (60 FPS patches, GoldHEN cheats, AFR asset redirection, and PRX mod menus) for Grand Theft Auto V (CUSA00411/CUSA00419) on jailbroken PlayStation 4 consoles running GoldHEN (HEN 11.02).
---

# PS4 GTA V Modding Architecture & Engineering Runbook (`ps4-gtav-modder`)

## ⚡ Purpose & Capabilities
`ps4-gtav-modder` provides end-to-end technical procedures, memory invariants, and asset redirection rules for modding **Grand Theft Auto V** (`CUSA00411` EUR / `CUSA00419` USA) on jailbroken PlayStation 4 consoles running **GoldHEN v2.4b (HEN 11.02)**.

Primary Implementation Repository: [**`GoldSantos` (GitHub)**](https://github.com/AICyberGuardian/GoldSantos).

---

## 🏛️ System & Engine Architecture

### 1. Invariant Baseline
* **Platform:** Sony PlayStation 4 (Fat CUH-1001A / Slim / Pro) on Orbis OS (FreeBSD x86-64).
* **Payload:** GoldHEN v2.4b18.5+ with `game_patch.prx` and `afr.prx` support.
* **Network Isolation:** PSN access is strictly blocked at the router/DNS layer; LAN FTP (`<PS4_IP>:2121`) is used for payload/package transfer.
* **Decoupled Architecture Mandate:** Never use anonymous "pre-modded update PKGs" (which cause `CE-34878-0` kernel panics and disable R2 trigger input). Always run clean 1:1 retail builds (`@Opoisso893/Golemnight`) and apply modifications dynamically from the outside via GoldSantos.
* **Privacy & Portability Invariant:** Never hardcode absolute workstation drive paths or private console LAN IPs. All repository references must use portable relative paths, and network targets must use dynamic environment variables (`PS4_IP`) or CLI arguments (`--ip`). Pre-commit hooks (`tools/audit_privacy_and_secrets.py`) automatically enforce this.

---

## 🛠️ The 4 Modding Tiers on PS4 (`GoldSantos`)

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                       MODULAR PS4 MODDING STACK                             │
├────────────────────────────────┬────────────────────────────────────────────┤
│ Tier 1: XML Memory Patches     │ /data/GoldHEN/patches/xml/                 │
│ Tier 2: GoldHEN In-Game Cheats │ /data/GoldHEN/cheats/json/ & ps4trainer    │
│ Tier 3: GoldHEN AFR Asset Mods │ /data/GoldHEN/AFR/CUSA00411/update/        │
│ Tier 4: Native SPRX / PRX Menus│ /data/GoldHEN/plugins/ (OpenOrbis built)   │
└────────────────────────────────┴────────────────────────────────────────────┘
```

### Tier 1: In-Memory XML Patches (`game_patch.prx`)
* **Location on PS4:** `/data/GoldHEN/patches/xml/GrandTheftAutoV-Orbis.xml`
* **Features:**
  * `60 FPS Unlock`: Memory byte-mask (`AppVer="01.56"` / `mask`). Unlocks the 30 FPS cap. (Note: CPU-limited on base PS4; yields 40–55 FPS in dense traffic).
  * `Skip Intro Video & Legal Logos`: Bypasses opening video and boots straight to game.
  * `Enable Snow in Singleplayer`: Unlocks winter holiday weather and vehicle drift physics across Los Santos.
* **Activation:** Settings -> GoldHEN -> Plugin Settings -> Enable Plugins Loader: `ON` & Game Patch: `ON`.

### Tier 2: GoldHEN Memory Cheats (`.json` / `.mc4`)
* **Location on PS4:** `/data/GoldHEN/cheats/json/CUSA00411_01.56.json`
* **Features:** God Mode, Never Wanted (freeze police), Infinite Ammo, No Reload, Super Jump, Explosive/Incendiary Bullets, Moon Gravity, $2.14B Cash.
* **Trigger:** Hold `Share` button in-game or navigate to `http://<PS4_IP>:2801` via `ps4trainer.com`.
* **Version Rule:** Cheats are static virtual addresses in `eboot.bin`. A cheat file for 1.27 or 1.46 will crash on 1.56. Only load version-matched JSON files.

### Tier 3: GoldHEN Application File Redirector (AFR)
* **Location on PS4:** `/data/GoldHEN/AFR/CUSA00411/update/update.rpf`
* **The Container Rule:** GTA V does **NOT** read loose files (e.g. `/app0/handling.dat`). It reads monolithic archives (`/app0/update/update.rpf`).
* **Workflow for Visuals, Gore, and Handling:**
  1. Modify source assets in `afr/src/`:
     * `handling/handling_chaos_boost.meta`: 220+ MPH top speed, downforce, and drift traction.
     * `visualsettings/visualsettings_clean.dat`: Remove haze/smog, boost streetlight bloom and wet reflections.
     * `decals/peddamagedecals_config.meta`: 180s blood decal persistence and arterial spray.
  2. Inject into clean PS4 `update.rpf` using OpenIV or `rpftool`.
  3. Upload to `/data/GoldHEN/AFR/CUSA00411/update/update.rpf`.
  4. Enable `afr.prx` in `/data/GoldHEN/plugins.ini` under `[CUSA00411]`.

### Tier 4: Native SPRX / PRX Menus (Lotus / 2much4u / Oxagon)
* **Location on PS4:** `/data/GoldHEN/plugins/` + `/data/GoldHEN/plugins.ini`
* **Porting Invariant:** Rockstar changes native hashes and pointer tables on every update. Menus targeting 1.27 or 1.48 crash on 1.56. Use `plugins/lotus-base/` with the 1.56 crossmap table to compile `gtav_menu_156.prx` via OpenOrbis Toolchain.

---

## 🚀 1-Click Deployment
To deploy all verified patches and cheats directly to the console over LAN:
```powershell
uv run python tools/deploy_mod_stack_lan.py --ip <PS4_IP> --all
```

---

## 📋 Operational Runbook & Best Practices

1. **Sequential PKG Installation Order:**
   * `01_CUSA00411_Grand_Theft_Auto_V_Base_Game_v1.00.pkg`
   * `02_CUSA00411_Grand_Theft_Auto_V_Update_v1.56.pkg`
   * `03_CUSA00411_Grand_Theft_Auto_V_DLC_PreOrder_Bonus.pkg`
2. **Preventing FTP Timeout / Sleep:**
   * Before transferring massive 40GB+ packages over LAN:
     **Settings -> Power Save Settings -> Set Time Until PS4 Turns Off -> Set to "Do Not Turn Off"**.
3. **Save Protection:**
   * Always backup unmodded campaign progress using **Apollo Save Tool (`APOL00004`)** to USB before activating memory-altering cheats.