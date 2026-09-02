# GTA V PS4 Architecture & Crash Analysis Guide

## 1. Why Pre-Baked Modded Updates Crash (`CE-34878-0`)

On PS4 Orbis OS, `CE-34878-0` is the generic userland exception code triggered whenever a process encounters an unhandled segmentation fault, illegal instruction, or memory access violation (equivalent to `SIGSEGV` or `SIGILL` on Unix/FreeBSD).

### Root Causes in "Pre-Modded" PKG Updates:

```
┌─────────────────────────────────────────────────────────────────────────┐
│                    ANATOMY OF A CRASH ON PS4 ORBIS OS                   │
├─────────────────────────────────────────────────────────────────────────┤
│ 1. Native Hash Mismatch: Calling 0x48DA... (1.27) on 1.56 -> Jump to Null│
│ 2. Obsolete EBOOT Offset: Hardcoded Base + 0x1A2B3C points into .rodata │
│ 3. Script Global Shift: Mod writes to Global_262145 -> Corrupts Camera  │
│ 4. Stack Alignment Violation: x86-64 SYS-V ABI requires 16-byte align   │
│ 5. Memory Exhaustion: Adding heavy 4K textures exceeds PS4 unified APU  │
└─────────────────────────────────────────────────────────────────────────┘
```

1. **Obsolete Pointer Dereferencing:**
   Pre-baked PKGs (e.g., God's Blessing or old v1.51/v1.53 Frankenstein updates) embed modified `eboot.bin` binaries with hardcoded addresses from older builds. When the engine executes code at an outdated offset, it attempts to read unmapped memory or execute data pages without `PROT_EXEC`, causing an instant crash.

2. **R2 Trigger and Controller Input Interrupts:**
   Old mod menus hook into game loop callbacks or controller polling loops (`scePadRead` / `CPad::GetButtonState`). If the hook signature alters registers (`RBX`, `R12-R15` non-volatile registers) without saving/restoring them according to the x86-64 System V ABI, input state is clobbered, leading to dead triggers (unable to shoot or accelerate).

3. **Save Game & Keystone Incompatibilities:**
   Pre-baked updates often alter the application keystone or save game format versioning, preventing official saves or Apollo Save Tool resigning from mounting correctly without data corruption.

---

## 2. Decoupled GoldHEN Modding: The Superior Architecture

By keeping the official `@Opoisso893` v1.56 PKG completely clean and unmodified, all custom modifications are injected **from the outside** via GoldHEN's modular subsystems:

```
+-------------------------------------------------------------------------+
|                  Clean Vanilla Game (e.g. CUSA00411 v1.56)              |
+-------------------------------------------------------------------------+
       ^                               ^                           ^
       | In-Memory Hooks               | Virtual Mem Writes        | VFS File Redirect
+---------------+              +-----------------+         +-------------------+
|  game_patch   |              |  Cheat Manager  |         |      AFR.prx      |
|  (XML AOB)    |              |  (JSON Trainer) |         | (update.rpf hook) |
+---------------+              +-----------------+         +-------------------+
```

### Advantages:
* **100% Reversibility:** If a mod causes instability, toggling a single line in `plugins.ini` or deleting a file in `/data/` restores vanilla behavior instantly without reinstalling a 50+ GB PKG.
* **Granular Isolation:** Individual mods can be enabled or disabled one by one to pinpoint performance drops.
* **Firmware Safety:** Decoupled mods operate within userland sandbox boundaries on GoldHEN 2.4b without causing kernel panics or console hard resets.

---

## 3. GoldHEN Application File Redirector (AFR) Mechanics

### The "Loose File" Fallacy
Many novice guides claim you can drop loose files like:
```text
/data/GoldHEN/afs/CUSA00411/visualsettings.dat   <-- INCORRECT (Wrong path & container)
```

### The Correct AFR Protocol:
1. **Plugin Configuration:** Enabled via `/data/GoldHEN/plugins.ini`:
   ```ini
   [CUSA00411]
   /data/GoldHEN/plugins/afr.prx=true
   ```
2. **Directory Structure:** GoldHEN AFR looks in:
   ```text
   /data/GoldHEN/AFR/CUSA00411/
   ```
3. **VFS Interception:** AFR hooks standard FreeBSD filesystem calls (`sceKernelOpen`, `open`, `read`). GTA V requests files from `/app0/update/update.rpf`. When AFR is active and a file exists at `/data/GoldHEN/AFR/CUSA00411/update/update.rpf`, GoldHEN transparently redirects the file descriptor to the `/data/` copy.

4. **Container Rebuild Requirement:**
   Because GTA V accesses internal data files (`handling.meta`, `visualsettings.dat`, `peddamagedecals.rpf`) from within compressed RPF archives, modifications must be packed into a valid **PS4 `update.rpf`** archive.

---

## 4. Performance Budget on Base PS4 (CUH-1001A)

The base 2013 PS4 APU features:
* **CPU:** 8 Jaguar x86-64 cores @ 1.6 GHz (2 cores reserved by OS).
* **GPU:** 1.84 TFLOPs GCN (18 Compute Units @ 800 MHz).
* **RAM:** 8 GB GDDR5 unified memory (~5.5 GB available to games).

### Performance Impact by Mod Tier:

| Mod | CPU Load | GPU Load | RAM Usage | Verdict on Fat PS4 |
| :--- | :---: | :---: | :---: | :--- |
| **60 FPS Unlock** | **High** | Medium | Low | Dynamic 40–55 FPS (CPU limited in dense traffic) |
| **Skip Logos / Intro** | None | None | None | 100% Recommended |
| **Snow in Singleplayer** | Very Low | Low | Low | 100% Safe & Fun |
| **GoldHEN Memory Cheats** | None | None | Minimal | Safe when version matches 1.56 |
| **Handling Overhaul** | None | None | None | Safe (Pure math changes in `handling.meta`) |
| **Blood Decal Duration** | Low | Low | Low | Safe if texture resolutions remain stock |
| **Clean Haze / Smog Removal** | None | -5% (Improves) | None | Safe & improves image clarity |
| **Object Spooner (100+ props)**| High | Medium | Medium | Limit active spawned props < 50 |
| **City-Wide Riot War** | High | Medium | Low | May drop FPS in heavy firefights |
| **Heavy 4K Graphics / Shaders**| High | **Extreme** | **Fatal** | **Avoid** on Base PS4 (causes stutter/freeze) |
