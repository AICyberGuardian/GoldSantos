# Native PRX Mod Menu Architecture & Porting Manual

## 1. Ground Truth on GTA V PS4 Mod Menus

### The Lineage of PS4 GTA V Menus:

```
┌────────────────────────────────────────────────────────────────────────┐
│                      PS4 GTA V MENU EVOLUTION TIMELINE                 │
├────────────────────────────────────────────────────────────────────────┤
│ 2018-2019 (FW 4.05-5.05): Lamance / NotYourDopes / LTSMenu (Web Payloads)│
│                                 │                                      │
│ 2020-2022 (GoldHEN Era):   Scorpion v1.2B (by RF0oDxM0Dz, up to 1.50)  │
│                            Lotus SPRX (by illusion / 0x199, 1.27/1.48) │
│                                 │                                      │
│ 2023-2026 (v1.53-1.56+):   Orbx Engine -> Oxagon Lite (by RF0oDxM0Dz)  │
│                            (Targeted specifically for 1.53 & 1.56)     │
└────────────────────────────────────────────────────────────────────────┘
```

1. **Scorpion 1.2B is NOT 1.56:** Scorpion was the benchmark singleplayer menu for PS4, but its development under the "Scorpion" name ceased at **v1.50**. Attempting to load Scorpion 1.2B against a 1.56 `eboot.bin` dereferences shifted pointers, crashing with `CE-34878-0`.
2. **The Replacement Lineage:** The original developer of Scorpion (`RF0oDxM0Dz`) transitioned to **Orbx Engine** and subsequently **Oxagon Lite**, which explicitly target **v1.53 and v1.56**.
3. **Lotus 1.48 Dead-End:** Lotus (`0x199` / ported by illusion) only supports 1.27 and 1.48. There is no official public 1.56 Lotus `.sprx`.
4. **Custom 1.56 Recompilation:** To build an open-source 1.56 menu without commercial/paid forks, one must use **2much4u's Menu Base**, update the native cross-map table (`crossmap.h`), generate 1.56 native wrappers (`natives_156.h`), and compile via the **OpenOrbis Toolchain**.

---

## 2. OpenOrbis Workspace Layout (`lotus-base/`)

* `include/types.h`: Engine typedefs (Entity, Ped, Vehicle, Hash, `scrNativeCallContext`).
* `include/crossmap.h`: Cross-map translation table mapping legacy hashes to v1.56 hashes.
* `include/natives_156.h`: Native function declarations for Player, Vehicle, Weapon, World, and Graphics.
* `include/menu.h`: Menu UI state machine and submenus (DLC Vehicle Spawner, Teleports, Riot Mode).
* `src/menu.cpp`: Submenu rendering, vehicle model hash table (Oppressor Mk II, Deluxo, Vigilante), and teleport coordinates.
* `src/hooks.cpp` & `src/main.cpp`: GoldHEN PRX lifecycle and function hook installers.
* `Makefile`: OpenOrbis `orbis-clang++` build script targeting `x86_64-scei-ps4`.

---

## 3. How to Build & Deploy:

```bash
cd lotus-base
make
```

Outputs `gtav_menu_156.prx`. Reference it inside `/data/GoldHEN/plugins.ini` on your PS4:
```ini
[CUSA00411]
/data/GoldHEN/plugins/gtav_menu_156.prx=true
```
