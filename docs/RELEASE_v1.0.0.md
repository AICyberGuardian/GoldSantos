# 🌴 GoldSantos v1.0.0 — Initial Decoupled Release for GTA V (v1.56 / CUSA00411)

Welcome to the initial public release of **GoldSantos**, the modern decoupled modding suite & chaos engine designed specifically for Grand Theft Auto V v1.56 on PlayStation 4 running GoldHEN v2.4b (HEN 11.02 / 9.00 / 5.05).

---

## 🚀 Highlights & Features Included

### 🟢 Layer 1: In-Memory Engine Patches (`GrandTheftAutoV-Orbis.xml`)
* **60 FPS Framerate Unlock:** Uncaps the internal 30 FPS vsync frame pacing cap for v1.56 (`Offset="0x01B1E370"`). Note: CPU-limited on base PS4 APU (~40–55 FPS in dense scenes).
* **Skip Intro Logos & Legal Disclaimers:** Universal mask-based bypass straight to loading screen.
* **North Yankton Snow in Story Mode:** Activates holiday snow overlay, icy road handling, and tire tracks across Los Santos.

### 🟢 Layer 2: Real-Time GoldHEN Cheat Suite (`CUSA00411_01.56.json`)
* 11 verified memory cheats accessible via **Share Button** in-game:
  * `God Mode (Infinite Health)`
  * `Never Wanted (Cops Ignore)`
  * `Instant 5-Star Maximum Heat (Chaos Mode)`
  * `Infinite Ammo & No Weapon Reloading`
  * `Max Armor on Damage / Equip`
  * `Infinite Special Ability Bar (Franklin/Michael/Trevor)`
  * `Explosive Bullets & Heavy Kinetic Force`
  * `Super Jump (Sky High)`
  * `Fast Run & Unlimited Sprint`
  * `Moon Gravity (Low Gravity Stunts)`
  * `Max Cash to Wallet ($2,147,483,647)`

### 🟡 Layer 3: AFR Asset Staging (`afr/src/`)
* **`handling_chaos_boost.meta`:** 220+ MPH top speed, enhanced downforce, responsive drift traction, deformation armor.
* **`visualsettings_clean.dat`:** 0.00 brown smog/fog, crystal-clear mountain and skyline views, boosted streetlight bloom.
* **`timecycle_mods_clean.xml`:** Clear horizon atmospheric profile.
* **`peddamagedecals_config.meta`:** 180s blood decal lifetime, persistent pools, arterial spray chance.

### 🟡 Layer 4: OpenOrbis C++ Mod Menu Base (`plugins/lotus-base/`)
* 1.56 Native Cross-Map Table (`crossmap.h`) translating 1.27/1.48 hashes to 1.56.
* 1.56 Native Function Wrappers (`natives_156.h`).
* Menu UI Engine (`menu.cpp`) with D-Pad navigation.
* **DLC Vehicle Spawner:** Oppressor Mk II, Deluxo, Vigilante (Batmobile), Truffade Thrax, Benefactor Krieger, Progen Emerus, TM-02 Khanjali Tank, Scramjet, Buzzard Chopper.
* **Pedestrian Riot Mode & Teleports.**

---

## 📦 How to Install:

### Option A: 1-Click LAN Deployment
```powershell
uv run python tools/deploy_mod_stack_lan.py --ip <YOUR_PS4_IP> --all
```

### Option B: USB Drive Installation
1. Download `GoldSantos-v1.56-PS4.zip`.
2. Extract the `data/` folder directly to the root of a FAT32/exFAT USB drive (`usb0:/data/GoldHEN/...`).
3. Copy to `/data/GoldHEN/` on your PS4 HDD using Apollo Save Tool or PS4-Xplorer.
