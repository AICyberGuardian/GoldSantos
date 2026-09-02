# GTA V v1.56 Safe Chaos & Enhancement Roadmap

A phased progression model designed to maximize fun, physics absurdity, and visual clarity while guaranteeing 100% stability on base PS4 hardware (CUH-1001A).

```
===========================================================================
  PHASE 1 (VERIFIED NOW) ──> PHASE 2         ──> PHASE 3       ──> PHASE 4
  illusion Engine Patch      GoldHEN 1.56 Cheat   AFR Container     1.56 Native PRX
  • 60 FPS Unlock (CPU-lim)  • God Mode           • Rebuilt Meta    • Oxagon / Rebuilt
  • Skip Legal / Logos       • Never Wanted       • Clean Smog        2much4u Menu Base
  • Snow in Singleplayer     • Ammo & $2.14B      • Blood Decals    • DLC Car Spawner
===========================================================================
```

---

## 🟢 Phase 1: Engine Baseline & Performance (Active & Verified)

* **Goal:** Maximize frame rates, reduce boot friction, and provide atmospheric variety with zero crash risk.
* **Mechanism:** GoldHEN `game_patch.prx` with official `GrandTheftAutoV-Orbis.xml`.
* **Features:**
  1. **60 FPS Framerate Unlock:** Uncaps the internal 30 FPS vsync limiter (`AppVer="01.56"`). Note: CPU-limited on Fat PS4 APU (~40–55 FPS depending on scene complexity).
  2. **Skip Intro & Legal Warnings:** Bypasses opening logos directly into loading screen (`AppVer="mask"`).
  3. **Snow in Singleplayer:** Toggles North Yankton holiday snow overlay across Los Santos (`AppVer="mask"`).
* **Stability:** 🟢 **100% Stable (Pattern-based / Official illusion0001 patch).**

---

## 🟡 Phase 2: Native 1.56 GoldHEN Cheat Set

* **Goal:** Real-time on-demand god mode, weapon wheel fills, and police suppression without risking story save corruption.
* **Mechanism:** `/data/GoldHEN/cheats/json/CUSA00411_01.56.json` loaded into the GoldHEN Cheat Menu (`Share` button hold).
* **Cheat Parameters:**
  - `[God Mode / Invincibility]`: Locks health pointer to full damage immunity.
  - `[Never Wanted]`: Freezes police wanted stars at 0.
  - `[Infinite Ammo & No Reload]`: Prevents magazine and ammo decrement.
  - `[Max Cash to Wallet]`: Sets wallet balance to $2,147,483,647.
  - `[Explosive Bullets & Kinetic Force]`: High kinetic impact ragdoll physics.
* **Stability:** 🟢 **High (Safe memory writes; isolated from mission scripts).**

---

## 🟠 Phase 3: Controlled AFR Asset Container (`update.rpf`)

* **Goal:** Enhanced vehicle speeds, darker nights, clear horizons, and intense blood decals without touching base PKGs.
* **Mechanism:** GoldHEN `afr.prx` redirecting `/app0/update/update.rpf` to `/data/GoldHEN/AFR/CUSA00411/update/update.rpf`.
* **Assets Targeted:**
  1. **`common/data/handling.meta`:**
     - Increased top speed caps (bypass 120 MPH artificial limit).
     - Enhanced suspension stiffness and high-speed downforce.
     - Drift traction multiplier tuning.
  2. **`common/data/visualsettings.dat` & `timecycle_mods_1.xml`:**
     - Removed brown distance smog/fog ceiling.
     - Boosted streetlight and headlight reflection intensity.
  3. **`peddamagedecals.meta`:**
     - Extended blood splatter lifetime to 180 seconds.
     - High-velocity arterial splatter patterns.
* **Stability:** 🟡 **Moderate (Requires full update.rpf rebuild; easy 1-click rollback by deleting file in /data/).**

---

## 🔴 Phase 4: Native 1.56 PRX Mod Menu

* **Goal:** Full in-game menu with vehicle spawners (all GTA Online DLC cars), object spooners, and ped riot mode.
* **Mechanism:** OpenOrbis-compiled PRX (`gtav_menu_156.prx` or `Oxagon Lite 1.56`) loaded dynamically via `plugins.ini`.
* **Crucial Rule:**
  - **Do NOT load Scorpion 1.2B or Lotus 1.48** (they are hardcoded to older updates and cause `CE-34878-0`).
  - Use only builds specifically compiled against the **v1.56 native cross-map table**.
* **Target Features:**
  - **DLC Vehicle Spawner:** Spawns Oppressor Mk II, Batmobile (Vigilante), Deluxo, Krieger, Thrax with instant max tune.
  - **Pedestrian Riot Mode:** Civilians armed with heavy weaponry, max aggression, hostile to each other.
  - **Object Spooner:** Place custom stunt ramps and loops.
* **Stability:** 🟡 **High when compiled natively for 1.56; Fatal if loading legacy 1.48/1.50 binaries.**
