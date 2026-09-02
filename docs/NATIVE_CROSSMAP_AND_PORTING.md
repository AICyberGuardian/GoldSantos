# GTA V PS4 Native Cross-Mapping & Porting Specification

## 1. What Are Rockstar Natives?

Grand Theft Auto V scripts do not directly call raw engine C++ functions by fixed address. Instead, all game scripts (compiled `.ysc` files) and userland mods interact with the engine via a **Native Function Dispatcher** (`rage::scrEngine`).

Each native function (e.g., `CREATE_VEHICLE`, `SET_ENTITY_INVINCIBLE`, `GIVE_WEAPON_TO_PED`) is identified by a **64-bit uint64 cryptographic hash**:

```cpp
// Example: Invoking a native in C++
typedef void (*NativeHandler)(rage::scrNativeCallContext* context);

NativeHandler GetNativeHandler(uint64_t nativeHash);

void SET_ENTITY_INVINCIBLE(Entity entity, BOOL toggle) {
    rage::scrNativeCallContext context;
    context.Push(entity);
    context.Push(toggle);
    GetNativeHandler(0x6BC97F4F4D50EB04)(&context); // Native Hash for 1.56
}
```

---

## 2. The Version Problem: Native Hash Randomization

With every major update (e.g., v1.27 $\rightarrow$ v1.48 $\rightarrow$ v1.56), Rockstar runs an automated script that:
1. Re-hashes every native function identifier with a new random salt.
2. Shuffles the registration order in the internal native registration table (`g_nativeRegistrationTable`).
3. Shifts the virtual memory address of the dispatcher function `get_native_handler`.

```
┌────────────────────────────────────────────────────────────────────────┐
│                      NATIVE HASH MIGRATION PIPELINE                    │
├────────────────────────────────────────────────────────────────────────┤
│ v1.27 Hash: 0x48DA92019A82B340  (CREATE_VEHICLE)                       │
│    │                                                                   │
│    ├──> Cross-Map Lookup Table (PC / PS4 translation table)            │
│    │                                                                   │
│ v1.56 Hash: 0xAF35D0D2583051B0  (New 1.56 Hash)                       │
│    │                                                                   │
│    └──> Scanned against PS4 1.56 eboot.bin via Native Updater         │
│         └──> Generates updated `natives_156.h` for OpenOrbis compiler  │
└────────────────────────────────────────────────────────────────────────┘
```

---

## 3. Step-by-Step Porting Pipeline (Old Menu $\rightarrow$ 1.56 PRX)

### Step 1: Obtain Open-Source Menu Base
Do not attempt to reverse-engineer closed-source `.prx` files. Use well-documented open-source bases:
* **[2much4u PS4 GTA V Menu Base](https://github.com/2much4u/PS4-GTA-V-Menu-Base)** (Clean UI, button input, memory helpers).
* **[Lotus SPRX Base](https://github.com/illusionyy/PS4-GTAV-Lotus-SPRX-Release)** (Ported to GoldHEN PRX by illusion).

### Step 2: Extract & Disassemble GTA V v1.56 `eboot.bin`
1. Decrypt the official v1.56 `eboot.bin` from the PS4 console.
2. Load the ELF into **IDA Pro 7.7+** or **Ghidra**.
3. Locate the **Native Registration Table** and dispatcher:
   - Search for pattern signature:
     ```text
     48 8D 0D ?? ?? ?? ?? 48 8B D8 E8 ?? ?? ?? ?? 48 85 C0
     ```
   - This leads directly to `rage::scrEngine::RegisterNativeHandler`.

### Step 3: Run the Native Cross-Map Updater
1. Use `PS4-GTA-V-Native-Updater` with the v1.56 crossmap JSON/text mapping.
2. Map all standard native functions from v1.27/v1.48 to v1.56 hashes.
3. Output a freshly generated `include/natives_156.h`.

### Step 4: Resolve Global & Pointer Offsets
Direct engine pointers (World Pointer, Player Pointer, Global Script Table) cannot be updated via native crossmaps; they require manual address discovery:

| Pointer / Global | Purpose | Discovery Method |
| :--- | :--- | :--- |
| **`WorldPTR`** | Direct access to local player entity struct, coords, health | AOB pattern scan in `.text` segment |
| **`GlobalPTR`** | GTA V script global array (`Global_XXXXX`) | Pattern scan `rage::scrProgram::GetGlobal` |
| **`VehiclePool`** | Table of all active spawned vehicles in memory | Scan `CVehiclePool` constructor |
| **`PedPool`** | Table of all active pedestrians and NPCs | Scan `CPedPool` constructor |

### Step 5: Replace Fixed Offsets with AOB Pattern Scanning
Instead of hardcoding brittle addresses like:
```cpp
// Fragile (breaks on next patch)
uintptr_t pPlayer = *(uintptr_t*)(g_baseAddress + 0x0235B890);
```

Use resilient pattern matching:
```cpp
// Resilient (survives minor code shifts)
uintptr_t pPlayerPattern = Memory::FindPattern(
    "\x48\x8B\x05\x00\x00\x00\x00\x48\x8B\x48\x08\x48\x85\xC9\x74\x00",
    "xxx????xxxxxxxx?"
);
uintptr_t pPlayer = Memory::RipResolve(pPlayerPattern);
```

### Step 6: Compile with OpenOrbis Toolchain
1. Configure `Makefile` to target `Orbis-Clang` and link against `libkernel.prx`, `libScePad.prx`.
2. Produce `gtav_menu_156.prx`.
3. Deploy to `/data/GoldHEN/plugins/` and reference in `plugins.ini` under `[CUSA00411]`.

---

## 4. Key Open-Source References & Links

* **GoldHEN Plugin SDK:** `https://github.com/GoldHEN/GoldHEN_Plugins_SDK`
* **OpenOrbis PS4 Toolchain:** `https://github.com/OpenOrbis/OpenOrbis-PS4-Toolchain`
* **2much4u Menu Base:** `https://github.com/2much4u/PS4-GTA-V-Menu-Base`
* **2much4u Native Updater:** `https://github.com/2much4u/PS4-GTA-V-Native-Updater`
* **Lotus SPRX for GoldHEN:** `https://github.com/illusionyy/PS4-GTAV-Lotus-SPRX-Release`
* **MemDBG PS4 Memory Scanner:** `https://github.com/seregonwar/MemDBG`
